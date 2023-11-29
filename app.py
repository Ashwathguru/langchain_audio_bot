import streamlit as st
import sounddevice as sd
import speech_recognition as sr
import threading
import time

def get_input_devices():
    devices = sd.query_devices()
    input_devices = [device['name'] for device in devices if 'input' in device['name'].lower()]
    return input_devices

def record_audio(device_index):
    duration = 15  # seconds
    fs = 44100  # sampling rate
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=2, dtype='int16', device=device_index)
    sd.wait()

    return recording

def transcribe_audio(audio_data):
    recognizer = sr.Recognizer()
    audio = sr.AudioData(audio_data, sample_rate=44100, sample_width=2)
    
    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return "Speech Recognition could not understand audio"
    except sr.RequestError as e:
        return f"Error with the speech recognition service: {e}"

def main():
    st.title("Voice Recorder and Transcriber")

    input_devices = get_input_devices()
    device_index = st.selectbox("Select Input Device", input_devices, index=0)

    recording = None
    start_recording = st.button("Start Recording")

    if start_recording:
        st.info("Recording... Click 'Stop Recording' within 15 seconds.")
        recording = record_audio(input_devices.index(device_index))

    if recording is not None:
        st.success("Recording complete!")

        stop_recording = st.button("Stop Recording")

        if stop_recording:
            st.info("Processing... Please wait.")
            text = transcribe_audio(recording.tobytes())

            st.text_area("Transcribed Text", text, height=200)
            
            if st.button("Submit"):
                st.balloons()
                print("Transcribed Text:", text)

if __name__ == "__main__":
    main()
