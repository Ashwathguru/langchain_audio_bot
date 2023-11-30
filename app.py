import streamlit as st
import streamlit.components.v1 as components

# HTML and JS code for text input
html_code = """
<div>
    <label for="textInput">Enter Text:</label>
    <input type="text" id="textInput" name="textInput">
    <button onclick="sendText()">Submit</button>
</div>
<script>
    function sendText() {
        var inputValue = document.getElementById('textInput').value;
        Streamlit.setComponentValue(inputValue);
    }
</script>
"""

# Use Streamlit components to embed HTML and JS
text_input_component = components.html(html_code, height=100)

# Streamlit app
def main():
    st.title("Streamlit Share App with Text Input")

    # Streamlit component to get text input from HTML/JS
    user_input = st.text_input("Enter text:")
    st.write("You entered:", user_input)

    # Display the text input using HTML/JS
    st.markdown("<h3>HTML/JS Text Input:</h3>", unsafe_allow_html=True)
    text_input_component

if __name__ == "__main__":
    main()
