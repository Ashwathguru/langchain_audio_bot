import streamlit as st

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
        // Use Streamlit's StreamlitScriptRunner to send the input to the Python code
        Streamlit.scriptRunner.enqueue({
            task: "set_value",
            args: [["userInput"], inputValue],
        });
    }
</script>
"""

# Use Streamlit components to embed HTML and JS
st.components.v1.html(html_code, height=100)

# Streamlit app
def main():
    st.title("Streamlit Share App with Text Input")

    # Access the value set by the JavaScript
    user_input = st.session_state.get('userInput', "")

    # Display the text input
    st.write("You entered:", user_input)

if __name__ == "__main__":
    main()
