eel.expose(updatechattext);
function updatechattext(text1) {
    document.getElementById('chattext').value += '\n' + text1; 
}

eel.expose(updatespeaktext);
function updatespeaktext(text2) {
    document.getElementById('speaktext').value = text2; 
}

function appendToChatText() {
    eel.append_to_chattext(); 
}

function updateSpeakText() {
    eel.update_speaktext(); 
}
