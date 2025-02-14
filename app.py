import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests
import pandas as pd

# Set up Spotify API client
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id='ec66a64b68894a6f87c36c03e889ba49', 
                                               client_secret='7a465e16f3c94f2fbda3d52b5bff24dd',
                                               redirect_uri='http://localhost:8888/callback', 
                                               scope="user-top-read"))

# Fetch your Spotify top tracks
results = sp.current_user_top_tracks(limit=50, time_range='long_term')
tracks = results['items']

# Extract relevant features (genre, artist, track)
spotify_data = pd.DataFrame([{
    'track_name': track['name'],
    'artist': track['artists'][0]['name'],
    'popularity': track['popularity'],
    'track_id': track['id']
} for track in tracks])

# Fetch artist genres for each track using a separate function to avoid repeated API calls
def get_artist_genres(artist_name):
    artist = sp.search(q='artist:' + artist_name, type='artist', limit=1)
    if artist['artists']['items']:
        return artist['artists']['items'][0]['genres']
    return []

# Apply function to get genres for each artist
spotify_data['genres'] = spotify_data['artist'].apply(get_artist_genres)

# Print the Spotify data to check
print(spotify_data)

# Replace with your actual API key from Ticketmaster
api_key = 'vv2Wi8zdANbpanYvicrAJiSZfUMdw6SQ'

# Define the search parameters for Ticketmaster
params = {
    'apikey': api_key,  # Your API key
    'city': 'Melbourne',  # Search for events in Melbourne
    'classificationName': 'Music',  # Filter by music events
    'size': 100,  # Limit to 100 events
}

# Send the GET request to the Ticketmaster API
url = 'https://app.ticketmaster.com/discovery/v2/events.json'
response = requests.get(url, params=params)

# Check for successful response
if response.status_code == 200:
    events = response.json()  # Parse the JSON response
    event_data = []
    if '_embedded' in events and 'events' in events['_embedded']:
        for event in events['_embedded']['events']:
            event_name = event['name']
            event_date = event['dates']['start']['localDate']
            event_url = event['url']
            event_genre = event['classifications'][0]['genre']['name'] if 'classifications' in event else 'N/A'
            event_data.append({
                'event_name': event_name,
                'event_date': event_date,
                'event_url': event_url,
                'genre': event_genre
            })
    
    # Convert event data into a DataFrame
    event_df = pd.DataFrame(event_data)
    
    # Filter events based on the top genres from Spotify data
    top_genres = spotify_data['genres'].explode().value_counts().head(5).index.tolist()  # Get top 5 genres
    
    # Filter Ticketmaster events to match genres
    recommended_events = event_df[event_df['genre'].isin(top_genres)]
    
    # Print the recommended events
    print("Recommended Events Based on Your Top Tracks:")
    print(recommended_events[['event_name', 'event_date', 'event_url', 'genre']])

else:
    print(f"Error: {response.status_code} - {response.text}")

