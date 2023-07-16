import requests

def main():
    # Set the base URL of your Flask API
    base_url = 'http://127.0.0.1:5000'
    movie_name = 'Inception'  # Replace with the movie name you want to search

    try:
        # Make the GET request to the Flask API
        response = requests.get(f'{base_url}/movies/{movie_name}')

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Print the JSON response
            print(response.json())
        else:
            print(f"Failed to retrieve movie details. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error occurred during the request: {e}")

if __name__ == '__main__':
    main()
