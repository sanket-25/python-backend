from flask import Flask, request, jsonify
import requests
# from uuid import uuid4
from dotenv import load_dotenv
import os

app = Flask(__name__)

# Load environment variables from .env file
# load_dotenv()

# # Access API_KEY from environment variables
# API_KEY = os.getenv('API_KEY')

# Define a route for the homepage
@app.route('/')
def home():
    return 'Hello, world!'

# # Define a route to handle POST requests for chat completion
# @app.route('/api/chat', methods=['POST'])
# def chat_completion():
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

        # Extract the assistant's response
        assistant_response = chat_completion_data['choices'][0]['message']['content']

        return jsonify({'responseChat': assistant_response}), 200
    except Exception as e:
        print(e)
        return 'Error calling OpenAI API', 500

# if __name__ == '__main__':
#     port = int(os.environ.get('PORT', 5000))
#     app.run(host='0.0.0.0', port=port)
