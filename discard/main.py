# author:nerako
# Please use this program directly
# -----------------------2024.2.13-------------------------
import sys
import time
import TTS

import record_wav
import microphone_ASR
import wav_ASR
import F20_UI

# if __name__ == "__main__":
#     app = F20_UI.QApplication(sys.argv)
#     ex = F20_UI.dia_UI()
#     ex.update_text("hello can you hear me")
#     ex.update_text("can you work properly")
#     ex.update_text("can you work properly")
#     ex.update_text("can you work properly")
#     ex.update_status("I'm thinking")
#     sys.exit(app.exec_())

if __name__ == "__main__":
    # NEW_TTS = TTS.TTS()
    # NEW_TTS.speak("Conversational Agents and Spoken Language Processing")
    app = F20_UI.QApplication(sys.argv)
    ex = F20_UI.dia_UI()
    # ex.ASR_start()
    #for i in range(100):
    #    print(microphone_ASR.set_up())
    sys.exit(app.exec_())


