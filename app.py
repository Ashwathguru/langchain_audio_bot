import streamlit as st

def main():
    st.title("Streamlit App with Speech-to-Text")

    # Initialize the transcript variable
    transcript_input_key = "transcript_input_key"
    transcript_output_key = "transcript_output_key"

    transcript_input_placeholder = st.empty()
    transcript_input = transcript_input_placeholder.text_area("Transcript:", height=100, key=transcript_input_key)

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

    # Use st.form to handle the form submission
    with st.form("update_form"):
        # Check if the transcript has been updated and update the Python transcript variable
        if st.form_submit_button("Update Transcript"):
            updated_transcript = st.session_state.transcript_input_key
            transcript_input_placeholder.text_area("Transcript:", value=updated_transcript, height=100, key=transcript_output_key)

if __name__ == "__main__":
    main()
