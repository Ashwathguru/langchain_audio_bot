import streamlit as st
import speech_recognition as sr
import io
import soundfile as sf
import numpy as np

# Streamlit magic command to include the JavaScript code
st.markdown(
    """
    <script>
        let recorder;
        let chunks = [];

        function startRecording() {
            chunks = [];
            navigator.mediaDevices.getUserMedia({ audio: true })
                .then(function (stream) {
                    recorder = new MediaRecorder(stream);
                    recorder.ondataavailable = function (e) {
                        if (e.data.size > 0) {
                            chunks.push(e.data);
                        }
                    };
                    recorder.onstop = function () {
                        const audioBlob = new Blob(chunks, { type: 'audio/wav' });
                        const audioUrl = URL.createObjectURL(audioBlob);
                        Shiny.setInputValue('audio_data', audioUrl);
                    };
                    recorder.start();
                })
                .catch(function (err) {
                    console.error('Error accessing microphone', err);
                });
        }

        function stopRecording() {
            recorder.stop();
        }
    </script>
    """
)

def main():
    st.title("Audio Recorder and Transcriber")

    # Button to start recording
    if st.button("Start Recording"):
        st.markdown("Recording started! Speak into the microphone.")
        st.markdown("To stop recording, click the 'Stop Recording' button.")
        st.markdown("<button onclick='stopRecording()'>Stop Recording</button>", unsafe_allow_html=True)

    # Shiny component to receive audio data from JavaScript
    audio_data = st.shiny_input("audio_data")

    # Button to transcribe and save the audio
    if st.button("Transcribe and Save"):
        if audio_data is not None:
            text = transcribe_audio(audio_data)
            save_to_file(text)
            st.success("Audio transcribed and saved to 'sample.txt'")
        else:
            st.warning("No audio recorded!")

def transcribe_audio(audio_data):
    audio_array = st.audio_recorder(key="audio_recorder")
    audio_array = np.array(audio_array).T[0]  # Extract the audio data

    # Save audio to a temporary file
    with io.BytesIO() as wav_io:
        sf.write(wav_io, audio_array, samplerate=44100, format="wav")
        wav_io.seek(0)

        # Transcribe audio using Google Web Speech API
        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_io) as source:
            audio_text = recognizer.record(source)
            text = recognizer.recognize_google(audio_text)
        return text

def save_to_file(text):
    with open("sample.txt", "w") as file:
        file.write(text)

if __name__ == "__main__":
    main()
