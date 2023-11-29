import streamlit as st

html_code = """
<div>
    <p id="message">Initial Message</p>
    <button onclick="sendMessage()">Send Message</button>
</div>

<script>
    function sendMessage() {
        const message = prompt("Enter a new message:");
        if (message) {
            // Send the message to Streamlit
            Streamlit.setComponentValue({ name: 'message', data: message });
        }
    }

    // Listen for updates from Streamlit
    Streamlit.getComponentValue("message").then(data => {
        document.getElementById("message").innerText = data;
    });
</script>
"""

def main():
    st.title("Bi-Directional Communication Example")

    # Display the HTML component
    st.components.v1.html(html_code, height=200)

    # Get the updated message from the HTML component
    updated_message = st.session_state.message
    if updated_message:
        st.success(f"Updated Message: {updated_message}")

if __name__ == "__main__":
    main()
