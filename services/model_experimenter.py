import torch
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from models import ModelFactory
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.manifold import TSNE   
import numpy as np

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

        # Plot embeddings using t-SNE
        print("Plotting embeddings using t-SNE...")
        plot_embeddings(spotify_embeddings_np, event_embeddings_np)

       # Plot cosine similarity
        print("Plotting cosine similarity...")
        plot_cosine_similarity(spotify_embeddings_np, event_embeddings_np)

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

def plot_embeddings(spotify_embeddings_np, event_embeddings_np):
    # Combine Spotify and Event embeddings
    combined_embeddings = np.vstack((spotify_embeddings_np, event_embeddings_np))
    labels = ['Spotify'] * len(spotify_embeddings_np) + ['Event'] * len(event_embeddings_np)

    # Reduce dimensionality for visualization
    tsne = TSNE(n_components=2, random_state=42)
    reduced_embeddings = tsne.fit_transform(combined_embeddings)
    
    # Plot
    plt.figure(figsize=(10, 6))
    plt.scatter(reduced_embeddings[:, 0], reduced_embeddings[:, 1], c=['blue' if l == 'Spotify' else 'red' for l in labels])
    plt.title('t-SNE Visualization of Spotify and Event Embeddings')
    plt.legend(['Spotify Genres', 'Event Genres'])
    plt.show()


def plot_cosine_similarity(spotify_embeddings_np, event_embeddings_np):
    similarities = cosine_similarity(spotify_embeddings_np, event_embeddings_np)
    plt.figure(figsize=(12, 8))
    sns.heatmap(similarities, cmap='viridis')
    plt.title('Cosine Similarity Between Spotify Tracks and Events')
    plt.xlabel('Event Genres')
    plt.ylabel('Spotify Genres')
    plt.show()