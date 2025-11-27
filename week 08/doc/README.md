## Week 8: Database Implementation & Data Management

Student Name: AYANTU AYANA LETA
Student ID: M01059579
Course: CST1510 - CW2 - Multi-Domain Intelligence Platform

## Project Description

- Basically i did a SQLite database system that extends the Week 7 authentication system to include multi-domain data management for cyber incidents, datasets, and IT_tickets.

## What Was Built

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


## Results

- 4 users migrated and authenticated
- 3,247 total records loaded across all domains
- All CRUD operations tested and working
- Secure authentication maintained from Week 7