# author:nerako
# pip install SpeechRecognition
# The purpose of this project is to convert local recordings into text
# -----------------------2024.2.7-------------------------
from google.cloud import speech
import os
from retico_core import *
from retico_googleasr import *

def wav_to_text():
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "./KEY/f20ca-414109-a90efd88cea5.json"

    client = speech.SpeechClient()
    speech_file = "./SAVE/speaker.wav"
    with open(speech_file, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=44100,
        language_code="en-US",
    )

    operation = client.long_running_recognize(config=config, audio=audio)

    print("Waiting for operation to complete...")
    response = operation.result(timeout=90)

    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    for result in response.results:
        # The first alternative is the most likely one for this portion.
        print(u"Transcript: {}".format(result.alternatives[0].transcript))
        print("Confidence: {}".format(result.alternatives[0].confidence))

# wav_to_text()