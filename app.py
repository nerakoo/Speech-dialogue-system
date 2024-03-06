# author:nerako, David, Nedas
# For the main screen and UI, run this function directly.
# -----------------------2024.03.05-------------------------

import eel
import record_wav
import microphone_ASR
import wav_ASR
import TTS
from restaurant_manager import RestaurantManager


eel.init('web')
speaker = TTS.TTS()
rm = RestaurantManager()

def clar_request(slot):
    ans = rm.sendClarification(slot)
    eel.updatechattext(ans)
    speaker.speak(ans)
    mic_input = microphone_ASR.set_up()
    gpt_output = rm.sendSlotPrompt(mic_input)
    gpt_dict = rm.convert_stringtodict(gpt_output)
    print(gpt_output)
    rm.updateSlots(gpt_dict)
    print("Slots are: ", rm.restaurant_slots)
    print("response is: ", gpt_output)

@eel.expose
def append_to_chattext():
    eel.updatechattext("ChatGPT: Can I help you book a restaurant?")
    speaker.speak("Can I help you book a restaurant?")
    mic_input = microphone_ASR.set_up()
    # print("mic_input: ", mic_input)
    ans =  "speaker:" + mic_input
    # print("micinput: ", type(mic_input))
    eel.updatechattext(mic_input)
    gpt_output = rm.sendSlotPrompt(mic_input)
    gpt_dict = rm.convert_stringtodict(gpt_output)
    rm.updateSlots(gpt_dict)

    #while one of the slots is empty
    #list of each of the slots?
    '''for each slot
        if slot is not none:
            everything here'''

    print("Slots beginning: ", rm.restaurant_slots)


    keys = rm.check_empty_slots()
    print("first Keys are: ", keys)
    
    while keys:
        currKey = keys[0]
        print('currKey: ', currKey)
    #for slot in rm.restaurant_slots.keys():
        if rm.restaurant_slots[currKey] is None:
            quest =  rm.askForSlot(currKey)
            eel.updatechattext("ChatGPT: "+quest)
            speaker.speak(quest)
            mic_input = microphone_ASR.set_up()   
            eel.updatechattext("Speaker: " +mic_input)
            gpt_output = rm.sendSlotPrompt(mic_input)
            print(gpt_output)

            try:
                gpt_dict = rm.convert_stringtodict(gpt_output)
            except ValueError: 
                print("ValueError found... retrying...")
                print(gpt_output)
                gpt_output = rm.sendSlotPrompt(mic_input)
                gpt_dict = rm.convert_stringtodict(gpt_output)
                #clar_request(keys[0])
                print("Slots after error: ", rm.restaurant_slots)
        

        # keys = rm.check_empty_slots()
        #not getting updated properly
        rm.updateSlots(gpt_dict)
        keys = rm.check_empty_slots()
        print("Slots updated: ", rm.restaurant_slots)

        print("Keys are: ", keys)
        while currKey in keys:
            #while rm.restaurant_slots[currKey] is None:
            clar_request(currKey)
            print("Slots after looped clarification request: ", rm.restaurant_slots)
            #print("response is: ", gpt_output)
            keys = rm.check_empty_slots()
            print("Keys in loop are: ", keys)
            

            
        '''while rm.restaurant_slots[slot] is None:
            clar_request(slot) # not updateing
            #rm.updateSlots(gpt_dict)
            print("Slots after clarification request: ", rm.restaurant_slots)
            #print("response is: ", gpt_output)'''

    ans = "Convo Finished"
    eel.updatechattext(ans)
    speaker.speak(ans)

# @eel.expose
# def update_speaktext(ans):
#     eel.updatespeaktext(ans)


eel.start('index.html', size=(1100, 950))
