from flask import Flask, render_template, request, Response
import requests
from io import BytesIO

from flask import jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

API_URL_IMAGE_CAPTION = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-large"
API_URL_TTS = "https://api-inference.huggingface.co/models/facebook/mms-tts-eng"
HEADERS = {"Authorization": "Bearer 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"}

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS, PUT, PATCH, DELETE'
    return response


def get_image_caption(file_data):
    #import pdb; pdb.set_trace()
    response = requests.post(API_URL_IMAGE_CAPTION, headers=HEADERS, data=file_data)
    #print(response)
    return response.json()[0]['generated_text']

def get_tts_audio(text):
    #import pdb; pdb.set_trace()
    #print(text)
    payload = {"inputs": text}
    response = requests.post(API_URL_TTS, headers=HEADERS, json=payload)
    return response.content

@app.route('/')
def index():
    return "I'm Here"


@app.route('/process_image', methods=['GET', 'POST'])
def process_image():
    # try:

    #print(request.data)
    # print(request.data['file'])
    file = str(request.data).split('\\')[-1][:-1]
    
    if file:
        # Read file data
        print(file)
        with open(file, 'rb') as read_file:
            file_data = read_file.read()
        #print(file_data)
        #Get image caption
        caption = get_image_caption(file_data)
        print(caption)
        # Get text-to-speech audio
        audio_bytes = get_tts_audio(caption)
        #print(audio_bytes)
        # Save audio to a file (optional)
        with open("output.wav", "wb") as f:
            f.write(audio_bytes)

        # Create a response with the caption as plain text
        response = Response(caption, content_type='text/plain')
        # print(response)
        return response
    else:
        return "No file uploaded", 400
    # except Exception as e:
    #     print(f"Exception: {e}")
    #     return str(e), 500

if __name__ == '__main__':
    app.run(debug=False, host= "localhost", port= "8080")
