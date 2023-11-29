import streamlit as st

# Custom HTML and JavaScript code for speech-to-text
speech_to_text_code = """
<div>
    <button id="startSpeechToText">Start Speech to Text</button>
    <button id="stopSpeechToText" disabled>Stop Speech To Text</button>
</div>
<textarea id="transcriptionBox" rows="4" cols="50" readonly></textarea>

<script>
    let recognition;

    const startButton = document.getElementById("startSpeechToText");
    const stopButton = document.getElementById("stopSpeechToText");
    const transcriptionBox = document.getElementById("transcriptionBox");

    // Establish a connection to Streamlit
    const Streamlit = window.Streamlit;

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

        // Send the transcript to Streamlit
        Streamlit.setComponentValue({ name: "transcript", data: transcript });
    }
</script>
"""

def main():
    st.title("Streamlit App with Speech-to-Text")

    # Display the speech-to-text component
    st.components.v1.html(speech_to_text_code, height=200)

    # Receive the transcript from JavaScript
    transcript = st.components.v1.html("").transcript

    # Use the transcript variable in your Python code
    st.write("Transcript:", transcript)

if __name__ == "__main__":
    main()
