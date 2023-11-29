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
        // Send the transcript to the server using an HTTP request
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

def main():
    st.title("Streamlit App with Speech-to-Text")

    # Display the speech-to-text component
    st.components.v1.html(speech_to_text_code, height=200, scrolling=True)

    # Handle the HTTP request on the server side
    if st.button("Save Transcript"):
        transcript = st.text_area("Transcript:", key="transcript_key")
        save_to_file(transcript)

def save_to_file(transcript):
    # Handle the saving logic here, e.g., write to a file
    with open("transcript.txt", "w") as file:
        file.write(transcript)
    st.success("Transcript saved to file.")

if __name__ == "__main__":
    main()
