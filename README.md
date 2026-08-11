# Survey Management Platform

A web-based survey management platform built with Django and MongoDB for creating surveys, managing questions, collecting responses, and organizing user data.

## Overview

SondageApp is a Django-based web application designed to simplify the creation and management of online surveys.

The platform provides a structured environment where users can interact with surveys and submit their responses, while survey data and user information are managed through a backend connected to MongoDB.

The project also includes documentation covering the application's architecture, data flow, database setup, and development environment.

## Features

-  Create and manage surveys
-  Manage survey questions
-  User management
-  Collect and store survey responses
-  MongoDB database integration
-  Structured data flow between users, surveys, questions, and responses
-  Django-based web interface
-  Environment-based configuration
-  Setup and development documentation

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

Here’s your project description rewritten in clean Markdown format, ready to use in documentation or GitHub:



 Project Structure

sondageapp/ ├── sondage_app/          # Main Django application ├── sondages/             # Survey-related functionality ├── users/                # User management ├── templates/            # **HTML** templates ├── manage.py             # Django management script ├── requirements.txt      # Python dependencies ├── .env.example          # Environment variable template ├── .gitignore ├── COMPLETE_EXPLANATION.md ├── DATA_FLOW_EXAMPLE.md ├── HOW_TO_CHECK_ANSWERS.md ├── MONGODB_COMPASS_GUIDE.md ├── QUICK_START.md ├── README_MONGODB.md └── SETUP_INSTRUCTIONS.md

 Application Workflow

User

Browse / Access Survey

### Answer Questions

### Submit Responses

Store Survey Data → MongoDB

Entities:

Users

Surveys

Questions

Responses

 Database

MongoDB is used for storing application data.

Flexible document-oriented structure suitable for survey information.

Tools: MongoDB Compass for inspection and management.

 Installation

# Clone the repository

git clone [https://github.com/nisrineamroug/sondageapp.git](https://github.com/nisrineamroug/sondageapp.git) cd sondageapp

# Create virtual environment

python -m venv env

# Activate environment

# Windows env\Scripts\activate # Linux / macOS source env/bin/activate

# Install dependencies

pip install -r requirements.txt

# Configure environment variables

cp .env.example .env

Add MongoDB connection details in .env.

Verify connection using MongoDB Compass.

 Run the Application

python manage.py runserver

Access via Django’s local development server.

## Documentation

QUICK_START.md — Quick setup and usage guide

SETUP_INSTRUCTIONS.md — Environment and installation instructions

README_MONGODB.md — MongoDB configuration and usage

MONGODB_COMPASS_GUIDE.md — Database inspection guide

DATA_FLOW_EXAMPLE.md — Application data flow

HOW_TO_CHECK_ANSWERS.md — Working with submitted survey answers

COMPLETE_EXPLANATION.md — Detailed project explanation

## Learning Objectives

Develop web applications with Django

Design backend application structures

Work with NoSQL databases (MongoDB)

Integrate Django with MongoDB

Manage users and survey workflows

Configure applications via environment variables

Structure and document a professional web project
