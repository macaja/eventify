from spotify_api import get_spotify_client, get_user_top_tracks
from ticketmaster_api import get_events_by_city
from transformers import DistilBertTokenizer, DistilBertModel
import torch
import pandas as pd

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

    # Load DistilBERT tokenizer and model
    tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
    model = DistilBertModel.from_pretrained('distilbert-base-uncased')

    # Function to encode text
    def get_embeddings(text):
        inputs = tokenizer(text, return_tensors='pt', padding=True, truncation=True)
        outputs = model(**inputs)
        # Perform mean pooling to get a 2D tensor
        embeddings = torch.mean(outputs.last_hidden_state, dim=1).detach()
        return embeddings.squeeze(0)  # Remove extra dimension

    # Function to encode text

    # Get embeddings for Spotify genres and Ticketmaster event genres
    spotify_embeddings = (
        user_tracks.explode('genres')['genres']
        .dropna()  # Remove NaN values if any
        .loc[lambda x: x != '']  # Remove empty strings
        .apply(get_embeddings)
    )
    event_embeddings = events_by_city['genre'].apply(get_embeddings)

    # Compare similarity and recommend events
    from sklearn.metrics.pairwise import cosine_similarity

    # Convert embeddings to numpy arrays
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
    # Print recommended events as a DataFrame
    print("Recommended Events Based on Your Top Tracks:")
    print(pd.DataFrame(recommendations, columns=['Event Name', 'Event URL']))

if __name__ == '__main__':
    main()
