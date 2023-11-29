import streamlit as st

def main():
    st.title("Streamlit App with Speech-to-Text")

    # Initialize the transcript variable
    #transcript = st.text_area("Transcript:", height=100)

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

                // Send the transcript to Streamlit
                const transcript = transcriptionBox.value;
                Streamlit.setComponentValue({ name: "transcript", data: transcript });

                // Display the updated transcript using st.write
                Streamlit.setComponentValue({ name: "updateTranscript", data: true });
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

    # Display the speech-to-text component
    st.components.v1.html(speech_to_text_code, height=200)

    # Use st.form_submit_button to trigger updates
    with st.form("update_form"):
        st.form_submit_button("Update Transcript")

    # Check if the form was submitted and update the Python transcript variable
    if st.session_state.update_form:
        updated_transcript = st.session_state.transcript
        st.text_area("Transcript:", value=updated_transcript, height=100)

if __name__ == "__main__":
    main()
