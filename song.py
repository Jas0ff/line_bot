from msrest.authentication import CognitiveServicesCredentials

from linebot import LineBotApi, WebhookHandler
from linebot.models import *

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pyimgur

import io
import json
import time
from PIL import Image
import random

import env
import ai

import http.client, urllib.request, base64

headers = {
    # Request headers
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': f'{env.azure_api_key}',
}

body = {
    "url": "https://i.imgur.com/7aY6UqT.jpg"
}

params = urllib.parse.urlencode({
    'returnFaceId': 'false',
    'returnFaceLandmarks': 'false',
    'returnFaceAttributes': 'emotion, age',
    'recognitionModel': 'recognition_04',
    'returnRecognitionModel': 'false',
    'detectionModel': 'detection_01',
    'faceIdTimeToLive': '60',
})

line_bot_api = LineBotApi(env.line_access_token)
handler = WebhookHandler(env.line_secrete)

def upload(path):
    CLIENT_ID = env.imgur_client_id
    title = "temp img"
    im = pyimgur.Imgur(CLIENT_ID)
    uploaded_img = im.upload_image(path, title=title)
    return uploaded_img.link


def getsong():
    client_credentials_manager = SpotifyClientCredentials(client_id= env.spotify_id, client_secret=env.spotify_secrete)
    sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)
    playlist_id = '0vE2SkuKL2ECjbrxuO6DNr'
    songs = []
    for track in sp.playlist_tracks(playlist_id)['items']:
        track_name = track["track"]["name"]
        artist_name = track["track"]["artists"][0]["name"]
        song = str(track_name) + ' - ' + str(artist_name)
        songs.append(song)

    random.shuffle(songs)
    return songs[0]

    
def recognize_mood(imgdata):
    imgdata = io.BytesIO(imgdata)
    image = Image.open(imgdata)
    image.save(str(env.temp_dir)+'\\temp.png')
    body['url'] = env.website_url + '/get_img'

    try:
        conn = http.client.HTTPSConnection(env.azure_endpoint)
        conn.request("POST", "/face/v1.0/detect?%s" % params, f"{body}", headers)
        response = conn.getresponse()
        data = json.loads(response.read().decode('utf8')[1:-1])
        # print(data)
        age = int(data['faceAttributes']['age'])
        emotion = data['faceAttributes']['emotion']
        emotion = max(emotion, key=emotion.get)
        # print(age)
        # print(emotion)

        conn.close()
    except Exception as e:
        return -1, 'null'
    
    return age, emotion


def reply(event, age, mood):
    if age == -1:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='無法偵測心情')
        )
        return 

    emotion={
        'anger': '生氣',
        'contempt': '不屑',
        'disgust': '厭世',
        'fear': '害怕',
        'happiness': '開心',
        'neutral': '冷靜',
        'sadness': '傷心',
        'surprise': '驚訝'
    }

    response = f"你大概{age}歲,看起來蠻{emotion[mood]}的，推薦你這首: {getsong()}"

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=response)
    )


if __name__ == "__main__":
    print(env.temp_dir)


# KEY = env.azure_api_key
# ENDPOINT = env.azure_endpoint
# face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))


# def recognize_mood(imgdata):
#     imgdata = io.BytesIO(imgdata)
#     #detected_faces = face_client.face.detect_with_stream(imgdata)
#     img = 'https://images.unsplash.com/photo-1513303876354-9d34f07fc54f?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=387&q=80'
#     detected_faces = face_client.face.detect_with_url(url=img, detection_model='detection_03', recognition_model='recognition_04')

#     if len(detected_faces) ==0:
#         line_bot_api.reply_message(
#             event.reply_token,
#             TextSendMessage(text="未偵測到臉部表情")
#         )
#         return 
    
#     face = detected_faces[0]
#     print(face.face_attributes)
        

# if __name__ == '__main__':
#     img = 'https://images.unsplash.com/photo-1513303876354-9d34f07fc54f?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=387&q=80'
#     detected_faces = face_client.face.detect_with_url(url=img, detection_model='detection_01', recognition_model='recognition_04', return_face_attributes=['qualityForRecognition'])
#     face = detected_faces[0]
#     print(face.face_attributes)
#     face = detected_faces[0]
#     print(face.face_attributes)
    
