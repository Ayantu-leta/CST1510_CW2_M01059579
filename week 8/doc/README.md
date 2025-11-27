## Week 8: Database Implementation & Data Management

Student Name: AYANTU AYANA LETA
Student ID: M01059579
Course: CST1510 - CW2 - Multi-Domain Intelligence Platform

## Project Description

- Basically i did a SQLite database system that extends the Week 7 authentication system to include multi-domain data management for cyber incidents, datasets, and IT_tickets.


## Database Structure

- 4 Tables: Users, Cyber Incidents, Datasets, IT Tickets
- Secure Authentication: Integrated Week 7 bcrypt system
- Data Import: Loaded 481 incidents, 2,550 datasets, 216 tickets from CSV files

## Key Features

- User Management: Registration, login, role-based access
- CRUD Operations: Create, read, update, delete for all data
- Data Integrity: Parameterized queries, error handling
- Automated Setup: One-click database initialization

## Technical Stack

- Database: SQLite
- Security: bcrypt password hashing
- Data Handling: pandas for CSV import

## How the System Works

- You type a username and password.
- The system checks if the username and password are allowed
- The password is changed into a hash using bcrypt
- The system saves the username and the hash in users.txt
- When you log in, the system reads the file and checks the hash
- If the password is correct, you can log in

## Testing

- The code shows the original password and the hashed version.
- The code checks the password with the correct input.
- The code checks the password with the wrong input.

## Results

- 4 users migrated and authenticated
- 810 total records loaded across all domains
- All CRUD operations tested and working
