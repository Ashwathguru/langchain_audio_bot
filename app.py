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
        return transcript;
    }
</script>
"""

def main():
    st.title("Streamlit App with Speech-to-Text")

    # Display the speech-to-text component
    transcript = st.components.v1.html(speech_to_text_code, height=200)

    if transcript:
        # Display the stored transcribed text
        st.text(f"Stored Transcript: {transcript}")
        print(transcript)

if __name__ == "__main__":
    main()
