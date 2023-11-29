import streamlit as st

# Custom HTML and JavaScript code for speech-to-text
speech_to_text_code = """
<div>
    <button id="startSpeechToText">Start Speech to Text</button>
    <button id="stopSpeechToText" disabled>Stop Speech to Text</button>
</div>
<textarea id="transcriptionBox" rows="4" cols="50" readonly></textarea>

<script>
    let recognition;

    const startButton = document.getElementById("startSpeechToText");
    const stopButton = document.getElementById("stopSpeechToText");
    const transcriptionBox = document.getElementById("transcriptionBox");

    startButton.addEventListener("click", startSpeechToText);
    stopButton.addEventListener("click", stopSpeechToText);

    function startSpeechToText() {
        recognition = new window.webkitSpeechRecognition();
        recognition.onresult = handleSpeechResult;
        recognition.start();

        startButton.disabled = true;
        stopButton.disabled = false;
    }

    function stopSpeechToText() {
        if (recognition) {
            recognition.stop();
            startButton.disabled = false;
            stopButton.disabled = true;
        }
    }

    function handleSpeechResult(event) {
        const transcript = event.results[0][0].transcript;
        transcriptionBox.value = transcript;

        // Send the transcript to the Streamlit app
        Streamlit.setComponentValue(transcript);
    }
</script>
"""

class SessionState:
    transcript = ""

def main():
    st.title("Streamlit App with Speech-to-Text")

    # Display the speech-to-text component
    st.components.v1.html(speech_to_text_code, height=200)

    # Get the session state
    session_state = SessionState()

    # Display the stored transcribed text
    #st.text(f"Stored Transcript: {session_state.transcript}")

    # Display the real-time transcribed text
    real_time_transcript = st.text_area("Real-Time Transcription", value=session_state.transcript, height=100)
    session_state.transcript = real_time_transcript
    st.text(f"Stored Transcript: {session_state.transcript}")

if __name__ == "__main__":
    main()
