import streamlit as st
import os
import requests
import json

st.title("Music Chatbot")

# Set up the Spotify API credentials
client_id = "your_client_id_here"
client_secret = "your_client_secret_here"
access_token = ""

# Authenticate and get the access token
auth_response = requests.post('https://accounts.spotify.com/api/token', {
    'grant_type': 'client_credentials',
    'client_id': client_id,
    'client_secret': client_secret,
})

access_token = auth_response.json()['access_token']

# Define a function to search for songs of a given artist and return their URIs
def search_artist(artist):
    search_response = requests.get('https://api.spotify.com/v1/search', headers={
        'Authorization': f'Bearer {access_token}'
    }, params={
        'q': artist,
        'type': 'track'
    })

    song_uris = [item['uri'] for item in search_response.json()['tracks']['items']]
    return song_uris

# Define a function to generate a response for the chatbot
def generate_response(text):
    response = ""
    if "songs" in text and "artist" in text:
        artist = text["artist"]
        song_uris = search_artist(artist)
        response = f"Here are some popular songs by {artist}:"
        for song_uri in song_uris:
            response += f"\n - spotify:track:{song_uri.split(':')[-1]}"
    else:
        response = "Sorry, I didn't understand your request."
    return response

# Define the main function for the Streamlit app
def main():
    st.sidebar.title("Music Chatbot")
    user_input = st.text_input("Enter your message:")
    if user_input:
        text = {"artist": user_input}
        response = generate_response(text)
        st.write(response)

if __name__ == '__main__':
    main()
