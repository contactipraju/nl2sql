import os
import streamlit as st
import google.generativeai as genai

from utils.config import DEBUG, GEMINI_API_KEY

# Load Gemini API key from environment variable
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables.")
genai.configure(api_key=GEMINI_API_KEY)

# Initialize the model

# Switch to this model for more complex queries and accuracy (PROD)
# model = genai.GenerativeModel("gemini-2.5-pro")

model = genai.GenerativeModel("gemini-2.5-flash")

# --- Streamlit UI ---
st.set_page_config(page_title="Gemini Chatbot", page_icon="🤖", layout="centered")

st.title("🤖 Gemini Chatbot")
st.write("Chat with Google's Gemini model inside Streamlit!")

# Store chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display past messages
for msg in st.session_state.messages:
    role = "👤 You:" if msg["role"] == "user" else "🤖 Gemini:"
    st.markdown(f"**{role}** {msg['content']}")

# User input box
user_input = st.chat_input("Type your message...")

if user_input:
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Get Gemini response
    response = model.generate_content(user_input)
    gemini_reply = response.text

    # Add response to history
    st.session_state.messages.append({"role": "assistant", "content": gemini_reply})

    # Rerun app to refresh UI
    st.rerun()
