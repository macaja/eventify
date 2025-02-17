import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time

def get_spotify_client(client_id, client_secret, redirect_uri):
    """
    Returns a Spotify API client instance.
    """
    return spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope="user-top-read"
    ))

# Get top tracks from different time ranges
def get_user_top_tracks(sp):
    top_tracks = []
    time_ranges = ['short_term', 'medium_term', 'long_term']

    for time_range in time_ranges:
        for offset in range(0, 4000, 50):  # Paginate through more results
            results = sp.current_user_top_tracks(limit=50, offset=offset, time_range=time_range)
            if not results['items']:  # Stop if no more tracks are returned
                break
            top_tracks.extend(results['items'])
            time.sleep(0.5)  # Pause for half a second to avoid rate limits

    return top_tracks

# Function to extract relevant information
def prepare_track_data(tracks):
    track_data = []
    
    for track in tracks:
        track_info = {
            'track_id': track['id'],
            'track_name': track['name'],
            'artist_name': track['artists'][0]['name'],
            'album_name': track['album']['name'],
            'release_date': track['album']['release_date'],
            'popularity': track['popularity'],
            'track_url': track['external_urls']['spotify'],
            'artist_id': track['artists'][0]['id']  # Add artist ID for genre lookup
        }
        track_data.append(track_info)
    
    return track_data

# Get genres for all tracks in bulk
def add_genres_to_tracks(sp, track_data):
    """
    Adds genre information to each track by fetching the artist's genres in bulk.
    """
    # Collect unique artist IDs
    artist_ids = list({track['artist_id'] for track in track_data})
    
    # Spotify API allows fetching up to 50 artists at once
    artist_genres = {}
    for i in range(0, len(artist_ids), 50):
        batch = artist_ids[i:i+50]
        artists = sp.artists(batch)['artists']
        
        # Cache the genres for each artist
        for artist in artists:
            artist_genres[artist['id']] = artist['genres']
        
        time.sleep(0.5)  # Small delay to avoid hitting rate limits

    # Add genres to each track using cached results
    for track in track_data:
        track['genres'] = artist_genres.get(track['artist_id'], [])

    return track_data

def get_user_top_tracks_with_genres(sp):
    top_tracks = get_user_top_tracks(sp)
    tracks_data = prepare_track_data(top_tracks)
    return add_genres_to_tracks(sp, tracks_data)