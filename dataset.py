import requests
import json
import time
import pandas as pd
from tqdm import tqdm

# Define API endpoints
JOKE_API_ENDPOINTS = {
    "jokeapi": "https://v2.jokeapi.dev/joke/Any?blacklistFlags=nsfw,religious,political,racist,sexist,explicit&type=single",
    "icanhazdadjoke": "https://icanhazdadjoke.com/",
    "official_joke_api": "https://official-joke-api.appspot.com/random_joke"
}

# Headers for APIs that require them
HEADERS = {
    "jokeapi": {},
    "icanhazdadjoke": {"Accept": "application/json"},
    "official_joke_api": {}
}

# Create an empty DataFrame to store jokes
jokes_df = pd.DataFrame(columns=['joke_id', 'text', 'category', 'source'])

# Function to fetch jokes from JokeAPI
def fetch_from_jokeapi(num_jokes=100):
    jokes = []
    for _ in tqdm(range(num_jokes), desc="Fetching from JokeAPI"):
        try:
            response = requests.get(JOKE_API_ENDPOINTS["jokeapi"])
            data = response.json()
            
            if response.status_code == 200 and data.get("type") == "single":
                joke = {
                    'joke_id': data.get("id"),
                    'text': data.get("joke"),
                    'category': data.get("category"),
                    'source': "jokeapi"
                }
                jokes.append(joke)
            
            # Sleep to respect API rate limits
            time.sleep(1)
        except Exception as e:
            print(f"Error fetching from JokeAPI: {e}")
    
    return jokes

# Function to fetch jokes from icanhazdadjoke
def fetch_from_icanhazdadjoke(num_jokes=100):
    jokes = []
    for _ in tqdm(range(num_jokes), desc="Fetching from icanhazdadjoke"):
        try:
            response = requests.get(
                JOKE_API_ENDPOINTS["icanhazdadjoke"], 
                headers=HEADERS["icanhazdadjoke"]
            )
            data = response.json()
            
            if response.status_code == 200:
                joke = {
                    'joke_id': data.get("id"),
                    'text': data.get("joke"),
                    'category': "Dad Joke",
                    'source': "icanhazdadjoke"
                }
                jokes.append(joke)
            
            # Sleep to respect API rate limits
            time.sleep(1)
        except Exception as e:
            print(f"Error fetching from icanhazdadjoke: {e}")
    
    return jokes

# Function to fetch jokes from Official Joke API
def fetch_from_official_joke_api(num_jokes=100):
    jokes = []
    for _ in tqdm(range(num_jokes), desc="Fetching from Official Joke API"):
        try:
            response = requests.get(JOKE_API_ENDPOINTS["official_joke_api"])
            data = response.json()
            
            if response.status_code == 200:
                joke = {
                    'joke_id': f"official_{len(jokes)}",  # Creating an ID
                    'text': f"{data.get('setup')} {data.get('punchline')}",
                    'category': data.get("type", "General"),
                    'source': "official_joke_api"
                }
                jokes.append(joke)
            
            # Sleep to respect API rate limits
            time.sleep(1)
        except Exception as e:
            print(f"Error fetching from Official Joke API: {e}")
    
    return jokes

# Fetch jokes from all sources
jokeapi_jokes = fetch_from_jokeapi(1000)
icanhazdadjoke_jokes = fetch_from_icanhazdadjoke(1000)
official_jokes = fetch_from_official_joke_api(1000)

# Combine all jokes
all_jokes = jokeapi_jokes + icanhazdadjoke_jokes + official_jokes

# Convert to DataFrame
jokes_df = pd.DataFrame(all_jokes)

# Remove duplicates based on text
jokes_df = jokes_df.drop_duplicates(subset=['text'])

# Save to CSV
jokes_df.to_csv('jokes_dataset_v2.csv', index=False)

print(f"Collected {len(jokes_df)} unique jokes and saved to jokes_dataset.csv")