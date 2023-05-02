import streamlit as st
import os
import requests
import json

# Set up the Spotify API credentials
client_id = "7302e978f89049e688d46fc635d928e8"
client_secret = "a6081fa4fdc4423b97bf2ceb699bbcbc"
access_token = ""


# Define a function to search for songs and return the top 5 results
def search_songs(artist):
    # Authenticate and get the access token
    auth_response = requests.post('https://accounts.spotify.com/api/token', {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
    })
    access_token = auth_response.json()['access_token']

    # Search for songs by the given artist and get the URIs of the top 5 results
    search_response = requests.get('https://api.spotify.com/v1/search', headers={
        'Authorization': f'Bearer {access_token}'
    }, params={
        'q': f'artist:{artist}',
        'type': 'track',
        'limit': 5
    })
    song_uris = [track['uri'] for track in search_response.json()['tracks']['items']]

    return song_uris


# Define the Streamlit app

st.title("Song Suggester")
st.write("Enter the name of an artist to get some song suggestions!")

# Get the input artist name from the user
artist_name = st.text_input("Artist name")

# If the user has entered an artist name, search for related songs and display them
if artist_name:
    st.write(f"Searching for songs by {artist_name}...")
    song_uris = search_songs(artist_name)
    if song_uris:
        st.write("Here are some song suggestions:")
        for uri in song_uris:
            st.write(uri)
    else:
        st.write("No songs found for this artist.")
