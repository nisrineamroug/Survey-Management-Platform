# Survey Management Platform

A web-based survey management platform built with Django and MongoDB for creating surveys, managing questions, collecting responses, and organizing user data.

## Overview

SondageApp is a Django-based web application designed to simplify the creation and management of online surveys.

The platform provides a structured environment where users can interact with surveys and submit their responses, while survey data and user information are managed through a backend connected to MongoDB.

The project also includes documentation covering the application's architecture, data flow, database setup, and development environment.

## Features

- 📝 Create and manage surveys
- ❓ Manage survey questions
- 👤 User management
- 📋 Collect and store survey responses
- 🗄️ MongoDB database integration
- 🔄 Structured data flow between users, surveys, questions, and responses
- 🌐 Django-based web interface
- ⚙️ Environment-based configuration
- 📚 Setup and development documentation

## Tech Stack

### Backend
- Python
- Django

### Database
- MongoDB
- MongoDB Compass

### Frontend
- HTML
- CSS
- Django Templates

### Development
- Git
- Python Virtual Environment
- Environment Variables

## Project Structure


sondageapp/
│
├── sondage_app/          # Main Django application
├── sondages/             # Survey-related functionality
├── users/                # User management
├── templates/            # HTML templates
├── manage.py             # Django management script
│
├── requirements.txt      # Python dependencies
├── .env.example          # Environment variable template
├── .gitignore
│
├── COMPLETE_EXPLANATION.md
├── DATA_FLOW_EXAMPLE.md
├── HOW_TO_CHECK_ANSWERS.md
├── MONGODB_COMPASS_GUIDE.md
├── QUICK_START.md
├── README_MONGODB.md
└── SETUP_INSTRUCTIONS.md


## Application Workflow

The application follows a simple survey workflow:

User
  │
  ▼
Browse / Access Survey
  │
  ▼
Answer Questions
  │
  ▼
Submit Responses
  │
  ▼
Store Survey Data
  │
  ▼
MongoDB

Survey-related entities are organized around users, surveys, questions, and responses, allowing collected data to be stored and managed in a structured way.

## Database

The project uses MongoDB for storing application data.

MongoDB provides a flexible document-oriented database structure suitable for storing survey-related information, including:

Users
Surveys
Questions
Responses

MongoDB Compass can be used to inspect and manage the database during development.

## Installation

1. Clone the repository
   
git clone https://github.com/nisrineamroug/Survey-Management-Platform.git

cd Survey-Management-Platform

3. Create a virtual environment
   
python -m venv env

4. Activate it:

Windows :

env\Scripts\activate

Linux / macOS :

source env/bin/activate

4. Install dependencies
   
pip install -r requirements.txt

5. Configure environment variables

Create a .env file based on the provided .env.example:

cp .env.example .env

On Windows, you can create the .env file manually if necessary.

Add the required configuration values for the application and MongoDB connection.

6. Configure MongoDB

Make sure MongoDB is available and configure the database connection according to the project's environment configuration.

MongoDB Compass can be used to verify the database connection and inspect stored data.

7. Run the application
python manage.py runserver

The application will then be available through the local Django development server.

Documentation

### The repository includes additional documentation covering different parts of the project:

QUICK_START.md — Quick setup and usage guide
SETUP_INSTRUCTIONS.md — Environment and installation instructions
README_MONGODB.md — MongoDB configuration and usage
MONGODB_COMPASS_GUIDE.md — Database inspection using MongoDB Compass
DATA_FLOW_EXAMPLE.md — Application data flow
HOW_TO_CHECK_ANSWERS.md — Working with submitted survey answers
COMPLETE_EXPLANATION.md — Detailed project explanation
Learning Objectives

### This project provided practical experience with:

Developing web applications with Django
Designing backend application structure
Working with NoSQL databases
Integrating Django with MongoDB
Managing users and application data
Handling survey and response workflows
Configuring applications through environment variables
Structuring and documenting a web development project
