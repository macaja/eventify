def populate_spotify_and_ticketmaster_model_data():
    from http_clients.spotify_api import get_spotify_client, get_user_top_tracks_with_genres
    from http_clients.ticketmaster_api import get_events_by_country
    from services.csv_writer import output_to_csv

    spotify_client_id = 'ec66a64b68894a6f87c36c03e889ba49'
    spotify_client_secret = '7a465e16f3c94f2fbda3d52b5bff24dd'
    redirect_uri = 'http://localhost:8888/callback'
    country_code = 'AU'
    
    sp = get_spotify_client(spotify_client_id, spotify_client_secret, redirect_uri)

    track_data_with_genres = get_user_top_tracks_with_genres(sp)

    spotify_tracks_output_file = 'spotify_tracks.csv'

    output_to_csv(track_data_with_genres, spotify_tracks_output_file)

    events_by_city = get_events_by_country(country_code)

    ticketmaster_events_output_file = 'ticketmaster_events.csv'

    output_to_csv(events_by_city, ticketmaster_events_output_file)