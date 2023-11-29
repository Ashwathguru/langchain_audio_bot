import streamlit as st

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
    </script>
    """

    st.components.v1.html(mic_js_code, height=0)

    st.text("Click the 'Start Recording' button and speak into your microphone.")

    # Output area to display the recognized text
    output_text = st.text_area("Recognized Text", "", key="mic-output")

    # Start and stop recording buttons
    if st.button("Start Recording"):
        st.info("Recording started...")

    if st.button("Stop Recording"):
        st.info("Recording stopped.")

    # Button to save the text to a file
    if st.button("Save to File"):
        saveToFile()
        st.info("Text saved to 'output.txt'")

if __name__ == "__main__":
    main()
