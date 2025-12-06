## Week 10: AI Integration with ChatGPT API
Student Name: AYANTU AYANA LETA  
Student ID: M01059579  
Course: CST1510 Multi Domain Intelligence Platform

## Project Description
Added an AI assistant page to the Multi Domain Intelligence Platform by integrating an AI assistant powered by OpenAIs ChatGPT API. The assistant provides specialized support across all four domains of the platform Cybersecurity, Data Science, It operations, and General Assistance it will expert guidance and real time analysis through a seamless chat interface.

## Features
- New ChatGPT page inside the my_app/pages
- ChatGPT API integration
- Streaming responses
- System prompt with domain control
- Chat history stored in session state
- Secure API key loading with secrets.toml
- Full support for cybersecurity and data analysis questions

## How It Works
- User logs in using Home.py
- Application loads the pages from the pages folder
- ChatGPT page reads the API key from secrets.toml
- Users choose their domain from Cybersecurity, Data Science, It operations, or General
- User enters a question in the chat box
- The model streams the reply in real time
- All conversation history is maintained in session state throughout the session

## Technical Stack
- Streamlit for the interface
- OpenAI Python library
- Session state for chat messages
- secrets.toml for API key
- SQLite database for the rest of the platform
- GPT-4.1-mini for efficient responses

## Results
- Working AI assistant inside the platform
- Real time streaming replies
- Stable integration with existing pages
- Secure API key handling