from config import API_INFO
import requests

# define the API endpoint and your API key. here weather data
weather_api_endpoint = "https://api.data.gov.in/resource/b3521980-43d8-4d22-b86e-43f9a927f4b9?"

"""
def get_initial_scroll_id():
    params = {
        "api-key": API_INFO["weather_api_key"],
        "format": "json",
        "scroll": "1m",
        "limit": 1000  # Ensure this matches the API's maximum limit
    }

    response = requests.get(weather_api_endpoint, params=params)

    # Print the entire response for debugging
    print(f"Status Code: {response.status_code}")
    print(f"Response Text: {response.text}")

    if response.status_code == 200:
        response_data = response.json()

        # Check if there are any error messages in the response
        if 'error' in response_data:
            raise Exception(f"API Error: {response_data['error']}")

        if '_scroll_id' in response_data:
            return response_data['_scroll_id']
        else:
            raise KeyError("Response does not contain '_scroll_id'.")
    else:
        raise Exception(f"API request failed with status code {response.status_code}")



def get_all_records(scroll_id):
    all_records = []

    while True:
        params = {
            'scroll': '1m',
            'scroll_id': scroll_id
        }
        response = requests.post('https://api.example.com/_search/scroll', json=params)
        data = response.json()

        # Print the response for debugging
        print(data)

        if 'hits' in data and 'hits' in data['hits']:
            records = data['hits']['hits']
            if not records:
                break  # No more records to retrieve
            all_records.extend(records)
            scroll_id = data['_scroll_id']  # Update scroll_id for next iteration
        else:
            break

    # Optionally clear the scroll context
    requests.delete('https://api.example.com/_search/scroll', json={'scroll_id': scroll_id})

    return all_records


try:
    initial_scroll_id = get_initial_scroll_id()
    all_records = get_all_records(initial_scroll_id)
    print(len(all_records))
except Exception as e:
    print(f"An error occurred: {e}")

"""
  # Replace with your actual endpoint

def get_all_records():
    """
    Perform pagination to retrieve all records from the API
    """
    params = {
        "api-key": API_INFO["weather_api_key"],
        "format": "json",
        "limit": 1000  # Smaller limit to ensure we don't hit the max window
    }
    offset = 0
    all_records = []
    total_retrieved = 0

    while True:
        params['offset'] = offset
        response = requests.get(weather_api_endpoint, params=params)

        if response.status_code != 200:
            print(f"API request failed with status code {response.status_code}")
            print(response.text)
            break

        data = response.json()

        if 'records' not in data or not data['records']:
            break  # No more records to retrieve

        records = data['records']
        all_records.extend(records)
        retrieved_records = len(records)
        total_retrieved += retrieved_records
        offset += retrieved_records  # Correctly update offset for the next batch

        # Print progress and first record for validation
        print(f"Retrieved {total_retrieved} records so far...")
        if records:
            print(f"First record: {records[0]}")

        # Break if no more records are returned
        if retrieved_records < params['limit']:
            break

    return all_records


# Example usage
try:
    all_records = get_all_records()
    print(f"Total records retrieved: {len(all_records)}")
except Exception as e:
    print(f"An error occurred: {e}")

