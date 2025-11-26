## Week 7: Secure Authentication System

Student Name: AYANTU AYANA LETA
Student ID:  M01059579
Course: CST1510 - CW2 - Multi-Domain Intelligence Platform

## Project Description

- A command-line authentication system implementing secure password hashing using the bcrypt library.
This system allows users to register accounts and log in with proper password verification.

## Features

- Secure password hashing using bcrypt with automatic salt generation
- User registration with duplicate username prevention
- User login with password verification
- Input validation for usernames and passwords
- File-based user data persistence using users.txt

## Technical Implementation

- Hashing Algorithm: bcrypt with automatic salting
- Data Storage: Plain text file (users.txt) with comma-separated values (username,hashed_password)
- Password Security: One-way hashing, no plaintext storage
- Validation: Username (3-20 alphanumeric characters), Password (6-50 characters, includes complexity check)

## How the System Works

- You type a username and password.
- The system checks if the username and password are allowed.
- The password is changed into a hash using bcrypt.
- The system saves the username and the hash in users.txt.
- When you log in, the system reads the file and checks the hash.
- If the password is correct, you can log in.

## Testing

- The code shows the original password and the hashed version.
- The code checks the password with the correct input.
- The code checks the password with the wrong input.
