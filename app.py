from spotify_api import get_spotify_client, get_user_top_tracks
from ticketmaster_api import get_events_by_city
import torch
import pandas as pd
from models import ModelFactory
from sklearn.metrics.pairwise import cosine_similarity

def main():
    spotify_client_id = 'ec66a64b68894a6f87c36c03e889ba49'
    spotify_client_secret = '7a465e16f3c94f2fbda3d52b5bff24dd'
    redirect_uri = 'http://localhost:8888/callback'
    city = 'Melbourne'
    
    sp = get_spotify_client(spotify_client_id, spotify_client_secret, redirect_uri)
    user_tracks = get_user_top_tracks(sp)
    
    user_tracks = pd.DataFrame(user_tracks)

    print(user_tracks)

    events_by_city = get_events_by_city(city)
    events_by_city = pd.DataFrame(events_by_city)

    print("\n#######################################################################################################################\n")

    print(events_by_city)

    # ... (rest of the code remains the same)

    model_factory = ModelFactory()
    models_to_test = ['distilbert', 'bert', 'roberta']  # Add more models as needed

    for model_name in models_to_test:
        model = model_factory.get_model(model_name)
        print(f"Testing {model_name} model...")

        # Get embeddings for Spotify genres and Ticketmaster event genres
        spotify_embeddings = (
            user_tracks.explode('genres')['genres']
            .dropna()  # Remove NaN values if any
            .loc[lambda x: x != '']  # Remove empty strings
            .apply(model.get_embeddings)
        )
        event_embeddings = events_by_city['genre'].apply(model.get_embeddings)

        # Compare similarity and recommend events
        spotify_embeddings_np = torch.stack(spotify_embeddings.tolist()).numpy()
        event_embeddings_np = torch.stack(event_embeddings.tolist()).numpy()

        recommendations = []
        for spotify_emb in spotify_embeddings_np:
            similarities = cosine_similarity([spotify_emb], event_embeddings_np)
            top_indices = similarities[0].argsort()[-5:][::-1]  # Get top 5 similar events

            for index in top_indices:
                event_name = events_by_city.iloc[index]['event_name']
                event_url = events_by_city.iloc[index]['event_url']
                recommendations.append([event_name, event_url])  # Store as a list of two elements

        print("\n#######################################################################################################################\n")
        print(f"Recommended Events Based on Your Top Tracks using {model_name} model:")
        print(pd.DataFrame(recommendations, columns=['Event Name', 'Event URL']))

if __name__ == '__main__':
    main()
