# author:nerako
# For the main screen and UI, run this function directly.
# -----------------------2024.2.18-------------------------

import eel
import record_wav
import microphone_ASR
import wav_ASR
import TTS

eel.init('web')
speaker = TTS.TTS()

@eel.expose
def append_to_chattext():
    ans = "speaker:" + microphone_ASR.set_up()
    eel.updatechattext(ans)
    ans = "chatgpt:hello,I have receive your message!"
    eel.updatechattext(ans)
    speaker.speak(ans)

# @eel.expose
# def update_speaktext(ans):
#     eel.updatespeaktext(ans)


eel.start('index.html', size=(1100, 850))
