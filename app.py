from flask import Flask, request, jsonify, render_template
from flask_pymongo import PyMongo
import requests
import os
from uuid import uuid4
from dotenv import load_dotenv
import base64

# Load environment variables from .env file
load_dotenv()

# Access API_KEY and GITHUB_TOKEN from environment variables
API_KEY = os.getenv('API_KEY')
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

app = Flask(__name__)

# MongoDB connection URI (replace <username>, <password>, and <dbname> with your MongoDB Atlas credentials)
app.config['MONGO_URI'] = 'mongodb+srv://2022sanketdhuri:WKm6WEKmHe80Mgql@cluster0.91iy5uo.mongodb.net/python'
mongo = PyMongo(app)

# Define a route for the homepage
@app.route('/')
def home():
    return 'Hello, world!'

# Define a route to handle POST requests for audio generation
@app.route('/api/audio', methods=['POST'])
def generate_audio():
    content = request.json.get('content')

    try:
        # Call the OpenAI API for chat completions
        chat_completion_response = requests.post('https://api.openai.com/v1/chat/completions', json={
            'model': 'gpt-3.5-turbo',
            'messages': [
                {'role': 'system', 'content': 'You are a helpful assistant.'},
                {'role': 'user', 'content': content}
            ]
        }, headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {API_KEY}'
        })

        chat_completion_data = chat_completion_response.json()

        # Call the OpenAI API for text-to-speech
        text_to_speech_response = requests.post('https://api.openai.com/v1/audio/speech', json={
            'model': 'tts-1',
            'input': chat_completion_data['choices'][0]['message']['content'],
            'voice': 'alloy'
        }, headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {API_KEY}'
        })

        # Generate a random file name
        file_name = str(uuid4()) + '.mp3'

        # Save the audio content to a file
        with open(file_name, 'wb') as file:
            file.write(text_to_speech_response.content)

        commit_message = f'[PYTHON]:{content}? -> {chat_completion_data["choices"][0]["message"]["content"]}'
        upload_to_github(file_name, commit_message)
        
        # Define the URLs
        audio_url = f'https://sanket-25.github.io/cdn/{file_name}'
        audio_download_url = f'https://raw.githubusercontent.com/sanket-25/cdn/main/{file_name}'

        # Save the audio file path to MongoDB
        data = {
            'userInput': content,
            'openAIResponse': chat_completion_data,
            'audioUrl': audio_url,
            'audioDownloadUrl': audio_download_url
        }
        mongo.db.Audio.insert_one(data)

        return jsonify({'audioUrl': audio_url, 'audioDownloadUrl': audio_download_url}), 200
    except Exception as e:
        print(e)
        return 'Error generating audio', 500

def upload_to_github(file_name, commit_message):
    try:
        file_content = open(file_name, 'rb').read()
        encoded_content = base64.b64encode(file_content).decode('utf-8')

        headers = {
            'Authorization': f'token {GITHUB_TOKEN}'
        }
        payload = {
            'message': commit_message,
            'content': encoded_content
        }
        response = requests.put(
            f'https://api.github.com/repos/sanket-25/cdn/contents/{file_name}',
            headers=headers,
            json=payload
        )
        response.raise_for_status()
    except Exception as e:
        print('Error uploading file to GitHub:', e)

# if __name__ == '__main__':
#     app.run()
