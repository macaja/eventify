import requests

def get_ticketmaster_api_key():
    return 'vv2Wi8zdANbpanYvicrAJiSZfUMdw6SQ'

def get_search_params(city, classification_name, size):
    api_key = get_ticketmaster_api_key()
    return {
        'apikey': api_key,
        'city': city,
        'classificationName': classification_name,
        'size': size
    }

def fetch_events(params):
    url = 'https://app.ticketmaster.com/discovery/v2/events.json'
    return requests.get(url, params=params)

def parse_event_data(response):
    if response.status_code == 200:
        events = response.json()
        if '_embedded' in events and 'events' in events['_embedded']:
            event_data = []
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
            return event_data
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return []
    
def get_events_by_city(city, size=100):
    params = get_search_params(city, 'Music', size)
    response = fetch_events(params)
    event_data = parse_event_data(response)
    return event_data
