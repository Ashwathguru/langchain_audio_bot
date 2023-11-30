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

def main():
    st.title("Streamlit App with Speech-to-Text")

    # Initialize session state
    if 'transcript' not in st.session_state:
        st.session_state.transcript = ""

    # Display the speech-to-text component
    st.components.v1.html(speech_to_text_code, height=200)

    # Display the transcript using st.markdown
    st.markdown(f"**Transcript:** {st.session_state.transcript}")

    # Use a Streamlit button to trigger saving the transcript to a file
    if st.button("Save Transcript to File") and st.session_state.transcript:
        with open("transcript.txt", "w") as file:
            file.write(st.session_state.transcript)

if __name__ == "__main__":
    main()
