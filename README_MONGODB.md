# Survey App - MongoDB Migration

This project has been migrated from MySQL to MongoDB (NoSQL) for Big Data course requirements.

## Changes Made

1. **Database**: Changed from MySQL to MongoDB
2. **ORM**: Using mongoengine instead of Django ORM for survey data
3. **Models**: Converted Django models to mongoengine Document models
4. **Views**: Updated to use mongoengine query syntax

## Setup Instructions

### 1. Install MongoDB
Download and install MongoDB from https://www.mongodb.com/try/download/community

Start MongoDB service:
```bash
# Windows (if installed as service, it should start automatically)
# Or use:
mongod

# Linux/Mac
sudo systemctl start mongod
# or
mongod --dbpath /path/to/data
```

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 3. Database Configuration
The app uses:
- **SQLite** for Django authentication (users, sessions)
- **MongoDB** for survey data (sondages, questions, responses)

MongoDB connection is configured in `sondage_app/__init__.py`:
- Database: `sondagesdb`
- Host: `localhost`
- Port: `27017`

### 4. Run Migrations (for SQLite - Django auth)
```bash
python manage.py migrate
```

### 5. Create Superuser
```bash
python manage.py createsuperuser
```

### 6. Run the Server
```bash
python manage.py runserver
```

## Model Changes

### Before (Django ORM with MySQL):
- Used `models.Model` with ForeignKey relationships
- Used Django's `.objects.filter()`, `.objects.create()` syntax

### After (mongoengine with MongoDB):
- Uses `Document` with `ReferenceField` relationships
- Uses `.objects()`, `.objects.create()` and direct instantiation with `.save()`

### Key Differences:
- Foreign keys store user IDs as integers (not references)
- Reverse relationships are accessed via properties or explicit queries
- ManyToMany becomes ListField of ReferenceFields
- Query syntax: `.objects.filter(x=y)` → `.objects(x=y)`

## Important Notes

1. Django Admin doesn't work with mongoengine models (commented out in admin.py)
2. Migrations are only needed for Django's SQLite database (auth)
3. MongoDB collections are created automatically when you save documents
4. User authentication still uses Django's built-in system with SQLite

## Testing

The application should work the same way as before, but now using MongoDB for data storage, which is more suitable for Big Data applications.

