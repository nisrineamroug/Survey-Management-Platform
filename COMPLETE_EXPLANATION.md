# Complete Guide: MySQL to MongoDB Migration - Everything You Need to Know

## Table of Contents
1. [What is NoSQL/MongoDB?](#what-is-nosqlmongodb)
2. [Why MongoDB for Big Data?](#why-mongodb-for-big-data)
3. [What Changed in Your Code?](#what-changed-in-your-code)
4. [MongoDB Compass - Your Data Viewer](#mongodb-compass---your-data-viewer)
5. [How to See Your Survey Data](#how-to-see-your-survey-data)
6. [Step-by-Step: Viewing Data After Survey Submission](#step-by-step-viewing-data-after-survey-submission)

---

## What is NoSQL/MongoDB?

### SQL vs NoSQL - Simple Explanation

**SQL (MySQL, PostgreSQL) - The Old Way:**
- Data is stored in **tables** (like Excel spreadsheets)
- Each row has the same columns
- Tables are connected by relationships (foreign keys)
- Very structured and rigid
- Example:
  ```
  Table: Sondage
  | id | title | description | user_id |
  |----|-------|-------------|---------|
  | 1  | Test  | My survey   | 5       |
  ```

**NoSQL (MongoDB) - The New Way:**
- Data is stored in **collections** (like folders)
- Each document (like a row) can have different fields
- More flexible - no fixed structure required
- Documents are stored as JSON (like JavaScript objects)
- Example:
  ```json
  {
    "_id": "507f1f77bcf86cd799439011",
    "title": "Test",
    "description": "My survey",
    "user_id": 5,
    "created_at": "2024-01-15T10:30:00Z"
  }
  ```

### Why MongoDB for Big Data?

MongoDB is **PERFECT** for Big Data because:
1. **Handles huge amounts of data** easily (millions/billions of documents)
2. **Fast** - designed for speed with large datasets
3. **Flexible** - can store different types of data together
4. **Scalable** - can distribute data across many servers
5. **JSON format** - easy to work with (very common in web development)

---

## What Changed in Your Code?

### 1. Database Connection (`sondage_app/__init__.py`)

**BEFORE (MySQL):**
```python
# Connection was handled by Django automatically in settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'sondagesdb',
        'USER': 'root',
        'PASSWORD': '...',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

**AFTER (MongoDB):**
```python
import mongoengine

# MongoDB connection - connects when Django starts
mongoengine.connect(
    db='sondagesdb',      # Database name
    host='localhost',      # Where MongoDB is running
    port=27017             # MongoDB default port
)
```

**What this means:** Instead of connecting to MySQL on port 3306, we now connect to MongoDB on port 27017.

---

### 2. Settings (`sondage_app/settings.py`)

**BEFORE:**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'sondagesdb',
        # ... MySQL config
    }
}
```

**AFTER:**
```python
# SQLite for Django authentication (users, login, sessions)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# MongoDB config for survey data
MONGODB_DB = 'sondagesdb'
MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
```

**Why two databases?**
- **SQLite** (small file-based database): Used ONLY for Django's built-in user authentication (login, sessions, permissions). This is easier and works fine for user management.
- **MongoDB**: Used for ALL your survey data (surveys, questions, answers). This is where the Big Data happens!

---

### 3. Models (`sondages/models.py`)

This is the BIGGEST change! Let me show you the difference:

#### BEFORE (Django ORM with MySQL):

```python
from django.db import models

class Sondage(models.Model):  # Inherits from Django Model
    title = models.CharField(max_length=200)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Links to User table
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
```

#### AFTER (Mongoengine with MongoDB):

```python
from mongoengine import Document, StringField, TextField, DateTimeField, IntField

class Sondage(Document):  # Inherits from mongoengine Document
    title = StringField(max_length=200, required=True)
    description = TextField(required=True)
    user_id = IntField(required=True)  # Stores user ID as integer (not a link)
    created_at = DateTimeField(default=timezone.now)
    
    meta = {'collection': 'sondages'}  # MongoDB collection name
    
    def __str__(self):
        return self.title
    
    @property
    def user(self):
        # Custom property to get the user from Django's user system
        from django.contrib.auth.models import User
        try:
            return User.objects.get(id=self.user_id)
        except User.DoesNotExist:
            return None
```

**Key Differences:**

| Django ORM (MySQL) | Mongoengine (MongoDB) |
|-------------------|----------------------|
| `models.Model` | `Document` |
| `models.CharField` | `StringField` |
| `models.TextField` | `TextField` |
| `models.ForeignKey` | `ReferenceField` or `IntField` (stores ID) |
| `models.DateTimeField` | `DateTimeField` |
| Tables | Collections (specified in `meta`) |

**Why user_id instead of ForeignKey?**
- MongoDB doesn't support joins like SQL databases
- We store the user's ID number instead of a link
- When we need the user, we look it up from Django's SQLite database

---

### 4. Views (`sondages/views.py`)

How we query data changed:

#### BEFORE (Django ORM):

```python
# Get all surveys for a user
my_sondages = Sondage.objects.filter(user=request.user)

# Get count
total_surveys = Sondage.objects.filter(user=request.user).count()

# Create new survey
sondage = Sondage.objects.create(
    title="My Survey",
    description="Description",
    user=request.user
)
```

#### AFTER (Mongoengine):

```python
# Get all surveys for a user (using user_id)
my_sondages = Sondage.objects(user_id=request.user.id)

# Get count
total_surveys = Sondage.objects(user_id=request.user.id).count()

# Create new survey
sondage = Sondage(
    title="My Survey",
    description="Description",
    user_id=request.user.id  # Store ID, not object
)
sondage.save()  # Must call .save() explicitly
```

**Key Differences:**

| Django ORM | Mongoengine |
|-----------|------------|
| `.objects.filter(user=x)` | `.objects(user_id=x.id)` |
| `.objects.create(...)` | Create object + `.save()` |
| `.objects.get(id=x)` | `.objects.get(id=x)` (similar) |
| `.objects.all()` | `.objects()` |

---

### 5. Forms (`sondages/forms.py`)

**BEFORE:**
```python
from django import forms
from .models import Sondage

class SondageForm(forms.ModelForm):  # Automatically creates form from model
    class Meta:
        model = Sondage
        fields = ['title', 'description']
```

**AFTER:**
```python
from django import forms

class SondageForm(forms.Form):  # Regular form (not ModelForm)
    title = forms.CharField(max_length=200, required=True)
    description = forms.CharField(widget=forms.Textarea, required=True)
```

**Why the change?**
- `ModelForm` requires Django models, but we're using mongoengine Documents
- We manually create forms and handle saving in the views

---

## MongoDB Compass - Your Data Viewer

### YES! You Should ABSOLUTELY Use MongoDB Compass!

**MongoDB Compass** is like "phpMyAdmin" for MySQL, but for MongoDB. It's a GUI (Graphical User Interface) that lets you:
- ✅ View all your data visually
- ✅ See collections (like tables)
- ✅ Browse documents (like rows)
- ✅ Search and filter data
- ✅ Edit data directly
- ✅ See database structure

### How to Use MongoDB Compass

1. **Open MongoDB Compass**
   - It should already be installed on your computer

2. **Connect to MongoDB**
   - Connection string: `mongodb://localhost:27017`
   - Or just click "Connect" (it uses default settings)

3. **Navigate to Your Database**
   - On the left sidebar, you'll see databases
   - Click on `sondagesdb` (your database name)
   - You'll see collections (like tables):
     - `sondages` - All your surveys
     - `questions` - All questions
     - `choices` - All answer choices
     - `reponses` - All survey responses
     - `answers` - Individual answers to questions

4. **View Data**
   - Click on any collection name
   - You'll see all documents (like rows in a table)
   - Each document shows as JSON (like a JavaScript object)

---

## How to See Your Survey Data

### After Someone Submits a Survey:

1. **Open MongoDB Compass**

2. **Connect to: `mongodb://localhost:27017`**

3. **Click on `sondagesdb` database**

4. **You'll see these collections:**

   #### Collection: `sondages`
   - Contains all survey information
   - Each document looks like:
     ```json
     {
       "_id": ObjectId("507f1f77bcf86cd799439011"),
       "title": "Customer Satisfaction Survey",
       "description": "Tell us about your experience",
       "user_id": 1,
       "created_at": ISODate("2024-01-15T10:30:00Z"),
       "shareable_link": UUID("a1b2c3d4-e5f6-...")
     }
     ```

   #### Collection: `questions`
   - Contains all questions from all surveys
   - Each document looks like:
     ```json
     {
       "_id": ObjectId("507f1f77bcf86cd799439012"),
       "sondage": ObjectId("507f1f77bcf86cd799439011"),  // Links to survey
       "text": "How satisfied are you?",
       "question_type": "scal",  // sc, mc, tx, or scal
       "min_value": 1,
       "max_value": 5
     }
     ```

   #### Collection: `reponses`
   - Contains each survey submission
   - Each document looks like:
     ```json
     {
       "_id": ObjectId("507f1f77bcf86cd799439013"),
       "sondage": ObjectId("507f1f77bcf86cd799439011"),  // Which survey
       "user_id": 2,  // Who submitted (or null if anonymous)
       "ip_address": "192.168.1.100",
       "date": ISODate("2024-01-15T11:00:00Z"),
       "created_at": ISODate("2024-01-15T11:00:00Z")
     }
     ```

   #### Collection: `answers`
   - Contains individual answers to each question
   - Each document looks like:
     ```json
     {
       "_id": ObjectId("507f1f77bcf86cd799439014"),
       "reponse": ObjectId("507f1f77bcf86cd799439013"),  // Which submission
       "question": ObjectId("507f1f77bcf86cd799439012"),  // Which question
       "texte": "5",  // For text/scale answers
       "choix": [  // For choice questions (multiple choice)
         ObjectId("507f1f77bcf86cd799439015")
       ]
     }
     ```

---

## Step-by-Step: Viewing Data After Survey Submission

### Scenario: Someone just submitted a survey

**Step 1: Open MongoDB Compass**
- Launch MongoDB Compass application

**Step 2: Connect**
- Click "Connect" (uses default: `mongodb://localhost:27017`)

**Step 3: Find Your Database**
- Look for `sondagesdb` in the left sidebar
- Click on it

**Step 4: Check the `reponses` Collection**
- Click on `reponses` collection
- You'll see a list of all survey submissions
- The most recent one will be at the top (usually)
- Each document shows:
  - When it was submitted (`date`, `created_at`)
  - Which survey (`sondage` - shows as ObjectId)
  - Who submitted it (`user_id` - or null)
  - IP address

**Step 5: Find the Answers**
- Click on `answers` collection
- Find answers where `reponse` matches the submission ID you saw
- Each answer shows:
  - Which question was answered (`question`)
  - The answer text (`texte`) or selected choices (`choix`)

**Step 6: Connect the Dots**
- To see the question text, look in `questions` collection
- Find the question with matching `_id`
- To see the survey name, look in `sondages` collection

### Pro Tip: Use Filters in Compass

You can filter data in MongoDB Compass:

1. **Find all responses for a specific survey:**
   - Go to `reponses` collection
   - Click "Filter" button
   - Enter: `{"sondage": ObjectId("507f1f77bcf86cd799439011")}`
   - Replace the ObjectId with your survey's ID

2. **Find all answers for a specific response:**
   - Go to `answers` collection
   - Click "Filter"
   - Enter: `{"reponse": ObjectId("507f1f77bcf86cd799439013")}`

3. **Find all questions for a survey:**
   - Go to `questions` collection
   - Click "Filter"
   - Enter: `{"sondage": ObjectId("507f1f77bcf86cd799439011")}`

---

## Visual Data Flow

```
User submits survey
        ↓
Creates: Reponse document in "reponses" collection
        ↓
For each question answered:
        ↓
Creates: Answer document in "answers" collection
        ↓
Links: Answer → Question → Sondage
        ↓
All data visible in MongoDB Compass!
```

---

## Summary

### What You Need to Remember:

1. **MongoDB stores data in collections** (not tables)
2. **Each document is like a JSON object** (flexible structure)
3. **MongoDB Compass shows everything** - it's your data viewer
4. **Your data structure:**
   - `sondages` → surveys
   - `questions` → questions in surveys
   - `reponses` → survey submissions
   - `answers` → individual answers
5. **Query syntax changed** from `.filter()` to `.objects()`
6. **Two databases:**
   - SQLite: User authentication
   - MongoDB: All survey data

### Quick Reference:

**Where is my data?**
- Open MongoDB Compass
- Connect to `mongodb://localhost:27017`
- Click on `sondagesdb`
- Browse collections to see everything!

**How do I see answers to a survey?**
1. Go to `reponses` collection → find the submission
2. Copy its `_id`
3. Go to `answers` collection → filter by `{"reponse": ObjectId("...")}`

**Is this good for Big Data?**
YES! MongoDB is designed for Big Data. It can handle millions of survey responses easily!

---

## Need Help?

- **MongoDB Compass won't connect?** Make sure MongoDB is running (`mongod` command)
- **Can't find your data?** Check that you're looking in the `sondagesdb` database
- **See ObjectIds instead of names?** That's normal! ObjectIds are MongoDB's way of identifying documents (like primary keys in SQL)

