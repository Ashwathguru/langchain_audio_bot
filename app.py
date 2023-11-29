import streamlit as st
import sounddevice as sd
import numpy as np
import speech_recognition as sr

def main():
    st.title("Audio Recorder and Transcriber")

    # Global variable to store recorded audio data
    recorded_audio_data = []

    start_recording_button = st.button("Start Recording")
    stop_recording_button = st.button("Stop Recording")

    if start_recording_button:
        st.success("Recording started! Speak into the microphone.")
        record_audio(recorded_audio_data)

    if stop_recording_button:
        st.warning("Recording stopped!")

        # Convert audio to text
        if recorded_audio_data:
            text = transcribe_audio(np.concatenate(recorded_audio_data))
            save_to_file(text)

            st.success("Audio transcribed and saved to 'sample.txt'")
        else:
            st.warning("No audio recorded!")

def record_audio(recorded_audio_data):
    # Sample rate and duration for recording
    sample_rate = 44100
    duration = 10  # You can adjust this as needed

    # Find the default input device
    input_device = sd.default.device[0]

    # Use a callback to append audio data to the global variable
    def callback(indata, frames, time, status):
        if status:
            print(status, flush=True)
        recorded_audio_data.append(indata.copy())

    # Start recording using sounddevice
    with sd.InputStream(device=input_device, channels=1, samplerate=sample_rate, callback=callback):
        sd.sleep(int(duration * 1000))

def transcribe_audio(audio_data):
    recognizer = sr.Recognizer()

    with sr.AudioFile(np.array(audio_data).tobytes()) as source:
        audio_text = recognizer.record(source)
        text = recognizer.recognize_google(audio_text)

    return text

def save_to_file(text):
    with open("sample.txt", "w") as file:
        file.write(text)

if __name__ == "__main__":
    main()
