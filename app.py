import streamlit as st
from flask import request
import requests

st.header('Friend')

url = "your_dialogflow_webhook_url_here"
headers = {"Content-Type": "application/json"}

response = requests.post(url, headers=headers, json=request.get_json())

data = response.json()
print(str(data))
