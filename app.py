import os
from google.cloud import dialogflow
import requests
import random
import streamlit as st
from flask import Flask, request, jsonify

DIALOGFLOW_PROJECT_ID = os.environ['ayan-jblc']
DIALOGFLOW_LANGUAGE_CODE = 'en'
SESSION_ID = 'me'

client_id = "7302e978f89049e688d46fc635d928e8"
client_secret = "a6081fa4fdc4423b97bf2ceb699bbcbc"
access_token = ""

app = Flask(__name__)

@app.route('/', methods=['POST'])
def search_songs():
    data = request.get_json()
    query = data['queryResult']['queryText']
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)
    text_input = dialogflow.types.TextInput(text=query, language_code=DIALOGFLOW_LANGUAGE_CODE)
    query_input = dialogflow.types.QueryInput(text=text_input)
    response = session_client.detect_intent(session=session, query_input=query_input)

    if response.query_result.intent.display_name == 'search_songs':
        artist = response.query_result.parameters.fields['music-artist'].string_value
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
        tracks = search_response.json()['tracks']['items']
        random.shuffle(tracks)
        song_links = [f'{track["name"]}-->{track["external_urls"]["spotify"]}" \n' for track in tracks]
        song_links_str = '\n'.join(song_links)
        fulfillment_text = f"Here are the top 5 songs by {artist}:\n{song_links_str}"
    else:
        fulfillment_text = "Sorry, I didn't understand that."

    response_data = {
        'fulfillmentText': fulfillment_text,
    }
    return jsonify(response_data)

if __name__ == '__main__':
    app.run()
