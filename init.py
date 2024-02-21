# author:nerako
# Auxiliary code
# -----------------------2024.2.20-------------------------

import eel
# import record_wav
# import microphone_ASR
# import wav_ASR

eel.init('web')

@eel.expose
def update_speaktext(ans):
    eel.updatespeaktext(ans)