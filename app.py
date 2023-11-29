import openai
import streamlit as st
from langchain.agents import create_csv_agent
from langchain.llms import OpenAI
import speech_recognition as sr

openai.api_key = st.secrets["OPENAI_API_KEY"]

def main():
    st.header("Chat with TicketGPT")
    st.title("Voice-to-Text App")

   # Button to start/stop microphone input
    if "stop" not in st.session_state:
        st.session_state.stop = False

    button_start = st.button("Start Microphone Input")
    button_stop = st.button("Stop Microphone Input")

    if button_start:
        st.session_state.stop = False
        st.experimental_rerun()

    if button_stop:
        st.session_state.stop = True

    if st.session_state.stop:
        st.stop()

    # Process voice input
    text = transcribe_microphone()
    st.text("Transcribed Text:")
    st.text(text)
    query = text
    button = st.button("Submit")
    if button:
      st.write(get_answer_csv(query))

def transcribe_microphone():
    recognizer = sr.Recognizer()

    # Capture audio from microphone with a 15-second timeout
    with sr.Microphone() as source:
        st.text("Listening... Speak something.")
        try:
            audio_data = recognizer.listen(source, timeout=15)
        except sr.WaitTimeoutError:
            return "Recording timed out after 15 seconds."

    # Recognize speech using Google Web Speech API
    try:
        text = recognizer.recognize_google(audio_data)
        return text
    except sr.UnknownValueError:
        return "Could not understand audio"
    except sr.RequestError as e:
        return f"Error connecting to Google Speech Recognition service: {e}"

def get_answer_csv(query: str) -> str:
    file = "raw.csv"
    agent = create_csv_agent(OpenAI(temperature=0), file, verbose=False)
    answer = agent.run(query)
    return answer

if __name__ == "__main__":
    main()






