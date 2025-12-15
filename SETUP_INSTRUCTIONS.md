# Complete Setup Guide - Get Everything Running

## Step-by-Step Instructions to Connect Everything

---

## Part 1: Install and Start MongoDB

### Step 1.1: Check if MongoDB is Installed

**Windows:**
1. Open Command Prompt or PowerShell
2. Type: `mongod --version`
3. If you see a version number, MongoDB is installed ✅
4. If you see "command not found", you need to install it

### Step 1.2: Install MongoDB (if not installed)

**Option A: Using MongoDB Installer (Recommended)**
1. Go to: https://www.mongodb.com/try/download/community
2. Select:
   - Version: Latest (7.0 or 6.0)
   - Platform: Windows
   - Package: MSI
3. Download and run the installer
4. During installation:
   - Choose "Complete" installation
   - ✅ Check "Install MongoDB as a Service"
   - ✅ Check "Install MongoDB Compass" (GUI tool)
5. Click "Install"

**Option B: Using Chocolatey (if you have it)**
```powershell
choco install mongodb
```

### Step 1.3: Start MongoDB Service

**Windows (if installed as service):**
- MongoDB should start automatically
- To check: Open Services (Win + R, type `services.msc`)
- Look for "MongoDB" service - it should be "Running"

**If not running automatically:**
1. Open Services
2. Find "MongoDB"
3. Right-click → Start

**Manual Start (if not installed as service):**
```powershell
# Open PowerShell as Administrator
mongod --dbpath "C:\data\db"
```
(You may need to create the folder first: `mkdir C:\data\db`)

### Step 1.4: Verify MongoDB is Running

1. Open a new Command Prompt/PowerShell
2. Type: `mongosh` (or `mongo` for older versions)
3. You should see: `>`
4. Type: `exit` to leave

**If this works, MongoDB is running! ✅**

---

## Part 2: Install Python Dependencies

### Step 2.1: Navigate to Your Project

```powershell
cd "C:\Users\halas\OneDrive\Bureau\sondage big data\sondageapp"
```

### Step 2.2: Activate Virtual Environment

```powershell
# Activate the virtual environment
.\env\Scripts\activate

# You should see (env) at the beginning of your prompt
```

### Step 2.3: Install Required Packages

```powershell
pip install -r requirements.txt
```

**If requirements.txt doesn't exist or has issues, install manually:**
```powershell
pip install Django==5.2.1
pip install mongoengine==0.27.0
pip install pymongo==4.6.0
pip install django-crispy-forms==2.4
pip install crispy-bootstrap5==2025.4
pip install python-dotenv==1.1.0
pip install pandas==2.2.3
pip install matplotlib==3.10.3
pip install xlsxwriter==3.2.3
pip install pillow==11.2.1
```

---

## Part 3: Configure Django Database

### Step 3.1: Run Django Migrations (for SQLite - User Authentication)

```powershell
python manage.py migrate
```

**This creates the SQLite database file (`db.sqlite3`) for user authentication.**

### Step 3.2: Create a Superuser (Admin Account)

```powershell
python manage.py createsuperuser
```

**Follow the prompts:**
- Username: (enter a username, e.g., `admin`)
- Email: (enter your email, or press Enter to skip)
- Password: (enter a password - it won't show as you type)
- Password (again): (confirm password)

**This creates an admin account to log into your website.**

---

## Part 4: Verify MongoDB Connection

### Step 4.1: Check MongoDB Connection Settings

**File: `sondage_app/__init__.py`**
```python
import mongoengine

# MongoDB connection
mongoengine.connect(
    db='sondagesdb',      # Database name
    host='localhost',     # MongoDB host
    port=27017            # MongoDB port
)
```

**This should already be correct!** ✅

### Step 4.2: Test MongoDB Connection

**Option A: Using Python (in Django shell)**
```powershell
python manage.py shell
```

Then type:
```python
from mongoengine import connect
connect('sondagesdb', host='localhost', port=27017)
print("Connected successfully!")
exit()
```

**Option B: Using MongoDB Compass**
- Open MongoDB Compass
- Connection string: `mongodb://localhost:27017`
- Click "Connect"
- You should see your databases listed

---

## Part 5: Start the Django Website

### Step 5.1: Make Sure Virtual Environment is Activated

```powershell
# You should see (env) at the start of your prompt
# If not, activate it:
.\env\Scripts\activate
```

### Step 5.2: Start the Development Server

```powershell
python manage.py runserver
```

**You should see:**
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

### Step 5.3: Open the Website

1. Open your web browser
2. Go to: `http://127.0.0.1:8000/` or `http://localhost:8000/`
3. You should see your survey application! ✅

---

## Part 6: Connect MongoDB Compass to View Data

### Step 6.1: Open MongoDB Compass

- If installed with MongoDB, find it in Start Menu
- Or download from: https://www.mongodb.com/try/download/compass

### Step 6.2: Connect to MongoDB

1. **Connection String:** `mongodb://localhost:27017`
   - Or just click "Connect" (uses default)
2. Click "Connect" button
3. You should see a list of databases

### Step 6.3: Find Your Database

1. Look for `sondagesdb` in the database list
2. Click on it
3. You'll see collections (they'll be empty until you create surveys):
   - `sondages`
   - `questions`
   - `choices`
   - `reponses`
   - `answers`

**Note:** Collections are created automatically when you save data!

---

## Part 7: Test Everything Works

### Step 7.1: Create a Survey on the Website

1. Go to: `http://localhost:8000/`
2. Log in (or register if you don't have an account)
3. Create a new survey
4. Add some questions
5. Save it

### Step 7.2: Check MongoDB Compass

1. Refresh MongoDB Compass (click refresh button)
2. Click on `sondagesdb`
3. Click on `sondages` collection
4. **You should see your survey!** ✅

### Step 7.3: Submit a Test Response

1. Get the survey link from your website
2. Open it in a new browser (or incognito mode)
3. Fill out and submit the survey

### Step 7.4: Check the Data in Compass

1. Go to `reponses` collection - you should see the submission
2. Go to `answers` collection - you should see the answers
3. **Everything is working!** ✅

---

## Troubleshooting

### Problem: "MongoDB connection failed"

**Solutions:**
1. Make sure MongoDB is running:
   ```powershell
   # Check if MongoDB service is running
   # Or start it manually:
   mongod
   ```

2. Check the port (should be 27017):
   ```powershell
   # In another terminal, test connection:
   mongosh
   ```

3. Check firewall settings (Windows might block MongoDB)

### Problem: "ModuleNotFoundError: No module named 'mongoengine'"

**Solution:**
```powershell
# Make sure virtual environment is activated
.\env\Scripts\activate

# Install mongoengine
pip install mongoengine
```

### Problem: "Database 'sondagesdb' doesn't exist"

**Solution:**
- This is normal! MongoDB creates databases automatically
- The database will be created when you save your first survey
- Just make sure MongoDB is running

### Problem: "Port 8000 already in use"

**Solution:**
```powershell
# Use a different port:
python manage.py runserver 8001
# Then go to: http://localhost:8001
```

### Problem: "Can't connect to MongoDB in Compass"

**Solutions:**
1. Make sure MongoDB is running (check Services)
2. Try connection string: `mongodb://127.0.0.1:27017`
3. Check if MongoDB is listening on port 27017:
   ```powershell
   netstat -an | findstr 27017
   ```

---

## Quick Start Checklist

Before running the website, make sure:

- [ ] MongoDB is installed
- [ ] MongoDB service is running (or `mongod` is running)
- [ ] Virtual environment is activated (`(env)` in prompt)
- [ ] All packages are installed (`pip install -r requirements.txt`)
- [ ] Django migrations are run (`python manage.py migrate`)
- [ ] Superuser is created (`python manage.py createsuperuser`)
- [ ] Django server is running (`python manage.py runserver`)
- [ ] MongoDB Compass is connected to `mongodb://localhost:27017`

---

## Daily Workflow

**Every time you want to work on the project:**

1. **Start MongoDB** (if not running as service):
   ```powershell
   mongod
   ```

2. **Open project folder:**
   ```powershell
   cd "C:\Users\halas\OneDrive\Bureau\sondage big data\sondageapp"
   ```

3. **Activate virtual environment:**
   ```powershell
   .\env\Scripts\activate
   ```

4. **Start Django server:**
   ```powershell
   python manage.py runserver
   ```

5. **Open browser:**
   - Go to: `http://localhost:8000/`

6. **Open MongoDB Compass** (optional, to view data):
   - Connect to: `mongodb://localhost:27017`
   - Browse `sondagesdb` database

---

## Connection Summary

### Website Connection:
- **URL:** `http://localhost:8000/`
- **Status:** Running when you see "Starting development server..."
- **Stop:** Press `CTRL+C` in the terminal

### MongoDB Connection:
- **Host:** `localhost`
- **Port:** `27017`
- **Database:** `sondagesdb`
- **Connection String:** `mongodb://localhost:27017`
- **Status:** Running when MongoDB service is active

### Django Connection to MongoDB:
- **Configured in:** `sondage_app/__init__.py`
- **Automatic:** Connects when Django starts
- **No action needed:** It's already set up!

---

## Need Help?

**Check if everything is running:**
1. MongoDB: Open MongoDB Compass → Should connect
2. Django: Browser shows website at `http://localhost:8000/`
3. Database: Create a survey → Check Compass → Should see data

**If something doesn't work:**
- Check the error message
- Make sure all services are running
- Verify you're in the correct folder
- Ensure virtual environment is activated

