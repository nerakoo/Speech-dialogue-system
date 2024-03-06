# author:nerako
# pip install SpeechRecognition
# What this project does is transcribe the sound directly into the microphone.
# -----------------------2024.2.13-------------------------

from __future__ import division

import os
import re
import sys
import time
import init
# import F20_UI
# import app
from google.cloud import speech
import pyaudio
import queue
from retico_core import *
from retico_googleasr import *
from evaluation import estimate_EO, estimate_RC, estimate_CT
"""
CODE FOR EVALUATION
"""
current_sentence = []
incremental_sentence = []
word_by_word = []
incre_word_by_word = []

language_code = "en-US"  # a BCP-47 language tag
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "./KEY/f20ca-414109-a90efd88cea5.json"
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

class MicrophoneStream(object):
    """Opens a recording stream as a generator yielding the audio chunks."""

    def __init__(self, rate, chunk):
        self._rate = rate
        self._chunk = chunk

        # Create a thread-safe buffer of audio data
        self._buff = queue.Queue()
        self.closed = True

    def __enter__(self):
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            # The API currently only supports 1-channel (mono) audio
            # https://goo.gl/z757pE
            channels=1,
            rate=self._rate,
            input=True,
            frames_per_buffer=self._chunk,
            # Run the audio stream asynchronously to fill the buffer object.
            # This is necessary so that the input device's buffer doesn't
            # overflow while the calling thread makes network requests, etc.
            stream_callback=self._fill_buffer,
        )

        self.closed = False

        return self

    def __exit__(self, type, value, traceback):
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self.closed = True
        # Signal the generator to terminate so that the client's
        # streaming_recognize method will not block the process termination.
        self._buff.put(None)
        self._audio_interface.terminate()

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        """Continuously collect data from the audio stream, into the buffer."""
        self._buff.put(in_data)
        return None, pyaudio.paContinue

    def generator(self):
        while not self.closed:
            # Use a blocking get() to ensure there's at least one chunk of
            # data, and stop iteration if the chunk is None, indicating the
            # end of the audio stream.
            chunk = self._buff.get()
            if chunk is None:
                return
            data = [chunk]

            # Now consume whatever other data's still buffered.
            while True:
                try:
                    chunk = self._buff.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                except queue.Empty:
                    break

            yield b"".join(data)

def sentence_to_text(responses):
    """
    CODE FOR EVALUATION
    """
    global current_sentence
    global incremental_sentence
    global word_by_word
    global incre_word_by_word

    num_chars_printed = 0
    for response in responses:
        if not response.results:
            continue

        result = response.results[0]
        if not result.alternatives:
            continue

        transcript = result.alternatives[0].transcript
        init.update_speaktext(transcript)
        # time.sleep(0.1)
        """
        CODE FOR EVALUATION
        """
        incremental_sentence.append(transcript)

        overwrite_chars = " " * (num_chars_printed - len(transcript))

        if not result.is_final:
            sys.stdout.write(transcript + overwrite_chars + "\r")
            sys.stdout.flush()

            num_chars_printed = len(transcript)

        else:
            """
            CODE FOR EVALUATION
            """
            for incre_sentence in incremental_sentence:
                incre_word_by_word.append(incre_sentence.split())
            # print(incremental_sentence)
            # print("***************************************************")

            # print(incre_word_by_word)
            # print("***************************************************")
            print(transcript + overwrite_chars)
            current_sentence.append(transcript + overwrite_chars)
            for sentence in current_sentence:
                word_by_word.append(sentence.split())

            # print("***************************************************")
            # print(word_by_word)

            w2w = word_by_word[0]
            iw2w = incre_word_by_word
            if(len(w2w) != 0):
                EO = estimate_EO(w2w, iw2w)
                print("============= EO: ", EO)

                RC = estimate_RC(w2w, iw2w)
                print("============= RC: ", RC)

                CTscore = estimate_CT(w2w, iw2w)
                print("============= CTscore: ", CTscore)

            print(transcript + overwrite_chars)
            answer = transcript + overwrite_chars
            num_chars_printed = 0

            """
            CODE FOR EVALUATION
            """
            current_sentence = []
            incremental_sentence = []
            word_by_word = []
            incre_word_by_word = []
            break

    return answer

def set_up():
    client = speech.SpeechClient()
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code=language_code,
    )

    streaming_config = speech.StreamingRecognitionConfig(
        config=config, interim_results=True
    )

    with MicrophoneStream(RATE, CHUNK) as stream:
        audio_generator = stream.generator()
        requests = (
            speech.StreamingRecognizeRequest(audio_content=content)
            for content in audio_generator
        )

        responses = client.streaming_recognize(streaming_config, requests)
        sentence = sentence_to_text(responses)
        return sentence
        # ex.update_text(sentence)
        # ex.Stop()

# def listen_print_loop(responses):
#     num_chars_printed = 0
#     for response in responses:
#         if not response.results:
#             continue
#
#         # The `results` list is consecutive. For streaming, we only care about
#         # the first result being considered, since once it's `is_final`, it
#         # moves on to considering the next utterance.
#         result = response.results[0]
#         if not result.alternatives:
#             continue
#
#         # Display the transcription of the top alternative.
#         transcript = result.alternatives[0].transcript
#
#         # Display interim results, but with a carriage return at the end of the
#         # line, so subsequent lines will overwrite them.
#         #
#         # If the previous result was longer than this one, we need to print
#         # some extra spaces to overwrite the previous result
#         overwrite_chars = " " * (num_chars_printed - len(transcript))
#
#         if not result.is_final:
#             sys.stdout.write(transcript + overwrite_chars + "\r")
#             sys.stdout.flush()
#
#             num_chars_printed = len(transcript)
#
#         else:
#             print(transcript + overwrite_chars)
#             answer = transcript + overwrite_chars
#             # ex.update_text(answer)
#
#             # Exit recognition if any of the transcribed phrases could be
#             # one of our keywords.
#             # if re.search(r"\b(exit|quit)\b", transcript, re.I):
#             #     print("Exiting..")
#             num_chars_printed = 0
#             break
#
#             num_chars_printed = 0



