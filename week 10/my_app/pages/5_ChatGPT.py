import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("AI Assistant")

#blocking the page if the user is not logged in 
if not st.session_state.logged_in:
    st.error("Login required")
    if st.button("Login"):
        st.switch_page("Home.py")
    st.stop()

# Domain selection
domain = st.selectbox(
    "Select Domain",
    ["General", "Cybersecurity", "Data Science", "it Operations"]
)

#cretaing system prompts for each domain
prompts = {
    "General": "You are a helpful assistant.",
    "Cybersecurity": "You are a cybersecurity expert assistant. Analyze incidents, threats, and provide technical guidance.",
    "Data Science": "You are a data science expert assistant. Help with analysis, visualization, and statistical insights.",
    "it Operations": "You are an IT operations expert assistant. Help troubleshoot issues, optimize systems, and manage tickets."
}

#it will initialize or update chat messages in session state
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": prompts[domain]}]
elif len(st.session_state.messages) > 0 and st.session_state.messages[0]["role"] == "system":

    st.session_state.messages[0]["content"] = prompts[domain]
elif len(st.session_state.messages) == 0:

    st.session_state.messages = [{"role": "system", "content": prompts[domain]}]

#displays all previous chat messages
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.write(message["content"])

#in the chat input box user types questions here
user = st.chat_input(f"Ask about {domain}...")

if user:

    st.session_state.messages.append({"role": "user", "content": user})
    
    #display users message in the chat
    with st.chat_message("user"):
        st.write(user)
    
 #get AI response
    reply = ""
    with st.chat_message("assistant"):
        container = st.empty()
        
 #it calls OpenAI API with streaming enabled
        completion = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=st.session_state.messages,
            stream=True
        )
        
 #it will process streaming response and show text as it arrives
        for chunk in completion:
            if chunk.choices[0].delta.content:
                reply += chunk.choices[0].delta.content
                container.write(reply)
    

    st.session_state.messages.append({"role": "assistant", "content": reply})


if st.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()