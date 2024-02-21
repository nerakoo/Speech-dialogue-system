# author:nerako
# pip install PyAudio
# The purpose of this project is to make local recordings
# -----------------------2024.2.7-------------------------
import wave
import pyaudio
from retico_core import *
from retico_googleasr import *

CHUNK = 1024  # Number of frames per buffer
FORMAT = pyaudio.paInt16  # The degree of discrimination of sound:8/16
CHANNELS = 1  # Single track
RATE = 44100  # Hz:44100/47250/48000

def record_audio(wave_out_path="./SAVE/speaker.wav", record_second=15):
    p = pyaudio.PyAudio()  # Instantiated object
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)  # Open the stream and pass in the response parameters
    wf = wave.open(wave_out_path, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)

    for _ in range(0, int(RATE * record_second / CHUNK)):
        data = stream.read(CHUNK)
        wf.writeframes(data)  # Write data
    stream.stop_stream()
    stream.close()
    p.terminate()
    wf.close()

# record_audio()