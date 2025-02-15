import spotipy
from spotipy.oauth2 import SpotifyOAuth

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

def get_user_top_tracks(sp, limit=50, time_range='long_term'):
    results = sp.current_user_top_tracks(limit=limit, time_range=time_range)
    tracks = results['items']
    track_data = []
    for track in tracks:
        track_name = track['name']
        track_artist = track['artists'][0]['name']
        track_album = track['album']['name']
        track_id = track['id']
        track_genres = get_track_genres(sp, track_id)
        track_data.append({
            'track_name': track_name,
            'track_artist': track_artist,
            'track_album': track_album,
            'track_id': track_id,
            'genres': track_genres
        })
    return track_data

def get_track_genres(sp, track_id):
    track_features = sp.track(track_id)
    track_artists = track_features['artists']
    artist_id = track_artists[0]['id']
    artist_info = sp.artist(artist_id)
    genres = artist_info['genres']
    return genres