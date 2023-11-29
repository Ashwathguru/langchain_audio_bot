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

            // Send the transcript to the server
            saveTranscript(transcriptionBox.value);
        }
    }

    function handleSpeechResult(event) {
        const transcript = event.results[0][0].transcript;
        transcriptionBox.value = transcript;
    }

    function saveTranscript(transcript) {
        // Send the transcript to the server using an HTTP POST request
        fetch('/save_transcript', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ transcript: transcript }),
        });
    }
</script>
"""

@st.server_route('/save_transcript', methods=['POST'])
def save_transcript():
    # Receive the transcript from the POST request
    data = st.request.json
    transcript = data.get('transcript')

    # Handle the transcript as needed (e.g., save to a file)
    if transcript:
        with open("transcript.txt", "w") as file:
            file.write(transcript)
        st.success("Transcript saved to file.")

def main():
    st.title("Streamlit App with Speech-to-Text")

    # Display the speech-to-text component
    st.components.v1.html(speech_to_text_code, height=200, scrolling=True)

if __name__ == "__main__":
    main()
