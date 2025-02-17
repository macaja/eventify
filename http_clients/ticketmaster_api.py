import requests
import time

def get_ticketmaster_api_key():
    return 'vv2Wi8zdANbpanYvicrAJiSZfUMdw6SQ'

def get_search_params(country_code, classification_name, size, page):
    api_key = get_ticketmaster_api_key()
    return {
        'apikey': api_key,
        'countryCode': country_code,  # Using countryCode instead of city for broader results
        'classificationName': classification_name,
        'size': size,
        'page': page
    }

def fetch_events(params):
    url = 'https://app.ticketmaster.com/discovery/v2/events.json'
    response = requests.get(url, params=params)
    return response

def parse_event_data(response):
    if response.status_code == 200:
        events = response.json()
        if '_embedded' in events and 'events' in events['_embedded']:
            event_data = []
            for event in events['_embedded']['events']:
                event_name = event['name']
                event_date = event['dates']['start']['localDate']
                event_url = event['url']
                event_genre = (event['classifications'][0]['genre']['name'] 
                               if 'classifications' in event and event['classifications'][0].get('genre') 
                               else 'N/A')
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

def get_events_by_country(country_code, total_events=1000):
    """
    Fetch at least `total_events` from Ticketmaster for the given country.
    """
    all_events = []
    page = 0
    size = 100  # Maximum allowed by Ticketmaster
    
    while len(all_events) < total_events:
        params = get_search_params(country_code, 'Music', size, page)
        response = fetch_events(params)
        event_data = parse_event_data(response)
        
        if not event_data:  # Stop if no more events are found
            print(f"No more events found on page {page}. Stopping.")
            break
        
        all_events.extend(event_data)
        page += 1  # Move to the next page
        
        print(f"Fetched {len(all_events)} events so far (Page {page})...")

        time.sleep(0.5)  # Small delay to avoid hitting rate limits
    
    return all_events[:total_events]  # Limit to requested number of events
