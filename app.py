import streamlit as st
from streamlit.report_thread import get_report_ctx
from streamlit.server.server import Server

def main():
    st.title("Streamlit App with Client-Side Microphone Access")

    # Custom HTML and JavaScript code to access the microphone
    mic_js_code = """
    <script>
        const recognition = new window.webkitSpeechRecognition();

        recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            document.getElementById('mic-output').value = transcript;
        };

        function startRecording() {
            recognition.start();
        }

        function stopRecording() {
            recognition.stop();
            updateStreamlitState();
        }

        function saveToFile() {
            const textToSave = document.getElementById('mic-output').value;
            const blob = new Blob([textToSave], { type: 'text/plain' });
            const a = document.createElement('a');
            a.href = URL.createObjectURL(blob);
            a.download = 'output.txt';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
        }

        function updateStreamlitState() {
            const transcript = document.getElementById('mic-output').value;
            Streamlit.setComponentValue(transcript);
        }
    </script>
    """

    st.components.v1.html(mic_js_code, height=0)

    st.text("Click the 'Start Recording' button and speak into your microphone.")

    # Output area to display the recognized text
    session_state = get_session_state()
    output_text = st.text_area("Recognized Text", session_state.transcript, key="mic-output")

    # Start and stop recording buttons
    if st.button("Start Recording"):
        session_state.transcript = ""
        st.info("Recording started...")

    if st.button("Stop Recording"):
        st.info("Recording stopped.")

    # Button to save the text to a file
    if st.button("Save to File", on_click="saveToFile()"):
        st.markdown(" <button onclick='saveToFile()'>Save to File</button>", unsafe_allow_html=True)

    # Display the recognized text after recording is done
    if session_state.transcript:
        st.success("Recognized Text:")
        st.write(session_state.transcript)

def get_session_state():
    session_id = get_report_ctx().session_id
    session_info = Server.get_current()._get_session_info(session_id)
    if session_info is None:
        return None
    session = session_info.session
    if not hasattr(session, "_custom_session_state"):
        session._custom_session_state = SessionState()
    return session._custom_session_state

class SessionState:
    transcript = ""

if __name__ == "__main__":
    main()
