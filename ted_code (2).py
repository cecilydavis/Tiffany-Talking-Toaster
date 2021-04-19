# Generic imports
import time
import os

# Dialogflow setup
import aiy.voice.tts 
import dialogflow_v2 as dialogflow
from aiy.board import Board
from aiy.cloudspeech import CloudSpeechClient

session_client = dialogflow.SessionsClient()
session = session_client.session_path('xxxxxxx', 12345)

# Servo setup
from gpiozero import Servo
rightEyebrowServo = Servo(26) 
leftEyebrowServo = Servo(24)


def getDialogResponse(text):

    text_input = dialogflow.types.TextInput(text=text, language_code='EN')

    query_input = dialogflow.types.QueryInput(text=text_input)

    response = session_client.detect_intent(session=session, query_input=query_input)

    text = response.query_result.fulfillment_text

    return response

def say(test):
    aiy.voice.tts.say(test, lang='en-US', volume=30, pitch=20, speed=80, device='default')

def angry():
    rightEyebrowServo.min()
    leftEyebrowServo.max()

def neutral():
    rightEyebrowServo.mid()
    leftEyebrowServo.mid()

def sad():
    rightEyebrowServo.max()
    leftEyebrowServo.min()

def sceptic():
    rightEyebrowServo.mid()
    leftEyebrowServo.max()

def frisky():
    neutral()
    time.sleep(0.1)
    for i in range(5):
        angry()
        time.sleep(0.1)
        sad()
        time.sleep(0.1)
    neutral()

def testEmotions():

    say("Angry")
    angry()
    time.sleep(2)

    say("Neutral")
    neutral()
    time.sleep(2)

    say("Sad")
    sad()
    time.sleep(2)

    say("sceptic")
    sceptic()
    time.sleep(2)

    say("frisky")
    frisky()
    time.sleep(2)


angry()

print('setup...')
client = CloudSpeechClient()

while True:

    print('Listening...')
    spokenText = client.recognize() 

    if spokenText is None:
        print('You said nothing.')
    else:
        response = getDialogResponse(spokenText)
        responseText = response.query_result.fulfillment_text
        responseIntent = response.query_result.intent.display_name
        responseIntentEmtion = responseIntent.split("_",1)[1].lower()

        if responseIntentEmtion == 'sceptic':
            sceptic()
        elif responseIntentEmtion == 'angry':
            angry()
        elif responseIntentEmtion == 'neutral':
            neutral()
        elif responseIntentEmtion == 'sad':
            sad()
        
        say(responseText)
        if responseIntentEmtion == 'frisky':
            frisky()

        angry()
    
    time.sleep(2)