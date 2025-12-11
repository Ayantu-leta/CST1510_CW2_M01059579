import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("AI Assistant 🤖")

#blocking the page if the user is not logged in 
if not st.session_state.get("logged_in"):
    st.error("Please login first")
    st.stop()

#get domain from button click or use default
domain = st.session_state.get("selected_domain", "General")
st.write(f"Domain: {domain}")

#system prompts for each domain
prompts = {
    "General": "You are a helpful assistant.",
    "Cybersecurity": "You are a cybersecurity expert. Help with security incidents, threats, and best practices.",
    "Data Science": "You are a data science expert. Help with data analysis, visualization, and ML.",
    "IT Operations": "You are an IT operations expert. Help with tickets, systems, and troubleshooting."
}

#initialize chat
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": prompts[domain]}]

#user input
user = st.chat_input(f"Ask about {domain}...")

if user:
    st.session_state.messages.append({"role": "user", "content": user})
    
    with st.chat_message("user"):
        st.write(user)
    
    with st.chat_message("assistant"):
        response = st.write_stream(client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=st.session_state.messages,
            stream=True
        ))
    
    st.session_state.messages.append({"role": "assistant", "content": response})

if st.button("Back to Home"):
    st.switch_page("Home.py")