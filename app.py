from services.model_data_retriever import populate_spotify_and_ticketmaster_model_data
from services.model_experimenter import recommend_events

def main():
    # populate_spotify_and_ticketmaster_model_data() # Uncomment this line if you want to populate the model data again

    user_tracks_file = 'model_data/spotify_tracks.csv'
    events_file = 'model_data/ticketmaster_events.csv'
    
    recommend_events(user_tracks_file, events_file)

if __name__ == '__main__':
    main()
