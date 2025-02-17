import torch
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from models import ModelFactory

def recommend_events(user_tracks_file, events_file, models_to_test=['distilbert']):
    # Load data from CSV files
    user_tracks = pd.read_csv(user_tracks_file)
    events_by_country = pd.read_csv(events_file)
    
    # Initialize ModelFactory
    model_factory = ModelFactory()
    recommendations_dict = {}

    # Loop through models to test
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
        event_embeddings = events_by_country['genre'].apply(model.get_embeddings)

        # Convert to NumPy arrays for similarity calculation
        spotify_embeddings_np = torch.stack(spotify_embeddings.tolist()).numpy()
        event_embeddings_np = torch.stack(event_embeddings.tolist()).numpy()

        # Calculate similarities and make recommendations
        recommendations = []
        for spotify_emb in spotify_embeddings_np:
            similarities = cosine_similarity([spotify_emb], event_embeddings_np)
            top_indices = similarities[0].argsort()[-5:][::-1]  # Get top 5 similar events

            for index in top_indices:
                event_name = events_by_country.iloc[index]['event_name']
                event_url = events_by_country.iloc[index]['event_url']
                recommendations.append([event_name, event_url])  # Store as a list of two elements

        recommendations_dict[model_name] = recommendations
        
        # Display recommendations
        print("\n#######################################################################################################################\n")
        print(f"Recommended Events Based on Your Top Tracks using {model_name} model:")
        print(pd.DataFrame(recommendations, columns=['Event Name', 'Event URL']))
    
    return recommendations_dict
