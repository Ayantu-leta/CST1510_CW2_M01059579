## Week 11: AI Integration with ChatGPT API
Student Name: AYANTU AYANA LETA  
Student ID: M01059579  
Course: CST1510 Multi Domain Intelligence Platform

## Project Description

The Multi-Domain Intelligence Platform is a secure, web based application built with Python and Streamlit. It provides specialized interactive dashboards for three professional domains Cybersecurity, Data Science, and IT Operations. Users can log in manage domain specific data with full CRUD operations, analyze trends with interactive charts and receive expert guidance from an integrated AI assistant.

## Features

## Cybersecurity Dashboard

- it tracks the security incidents with severity levels
- Create, read, update, and delete security incidents
- Visualize incident distribution by severity and status
- Get cybersecurity specific guidance and analysis

## Data Science Dashboard

- manage datasets
- View dataset sizes in MB with automatic conversion
- Monitor dataset volume
- Analyze data distribution and trends

## IT Operations Dashboard

- Manage IT support tickets
- Handles the urgent, high, medium and low priority tickets
- Assign tickets to team members
- Track ticket progress from open to resolved

## Security Features

- bcrypt encryption for secure password storage
- Secure user session tracking
- Protected against common security vulnerabilities
- SQL injection prevention through parameterized queries

## How It Works

- User runs the code from Home.py page
- User will logs in with existing or registers a new account
- After login at the home page displays buttons to navigate to the Cybersecurity, Data Science or IT Operations dashboard

Inside the dashboard the user clicks one of three buttons

- CRUD To perform Create, Read, Update, Delete operations on domain data
- To view the interactive graphs and data summaries
- and open a chat interface for domain specific AI guidance

## Technologies Used

- Streamlit 
- SQLite with SQLite3
- bcrypt password hashing
- OpenAI GPT API
- Streamlit charts
- GPT-4.1-mini 