import streamlit as st
import requests

st.header('Friend')

data = st.text_input('Enter your message here')

url = 'https://arnab2012-friend-chatbot-app-vkyz89.streamlit.app/'
headers = {'Content-Type': 'application/json'}

data = {
    'message': data,
    'sender': 'streamlit'
}

response = requests.post(url, headers=headers, json=data)

if response.ok:
    response_data = response.json()
    st.write(response_data['response'])
else:
    st.write('Error:', response.status_code)
