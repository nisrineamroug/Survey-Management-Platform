# Quick Start - Get Running in 5 Minutes

## 🚀 Fast Setup (Copy & Paste)

### 1. Start MongoDB
```powershell
# Check if running (should see version)
mongod --version

# If not running, start it:
mongod
# OR if installed as service, it's already running!
```

### 2. Navigate to Project & Activate Environment
```powershell
cd "C:\Users\halas\OneDrive\Bureau\sondage big data\sondageapp"
.\env\Scripts\activate
```

### 3. Install Packages (First Time Only)
```powershell
pip install -r requirements.txt
```

### 4. Setup Database (First Time Only)
```powershell
python manage.py migrate
python manage.py createsuperuser
```

### 5. Start Website
```powershell
python manage.py runserver
```

### 6. Open in Browser
- Go to: **http://localhost:8000/**

### 7. Open MongoDB Compass (Optional - to view data)
- Connection: **mongodb://localhost:27017**
- Database: **sondagesdb**

---

## 📍 Connection Details

| What | Where | How to Connect |
|------|-------|----------------|
| **Website** | http://localhost:8000/ | Open in browser |
| **MongoDB** | localhost:27017 | MongoDB Compass |
| **Database Name** | sondagesdb | Auto-created when you save data |
| **Django Admin** | http://localhost:8000/admin/ | Use superuser credentials |

---

## ✅ Quick Check - Is Everything Running?

1. **MongoDB Running?**
   - Open MongoDB Compass → Connect → Should work ✅

2. **Django Running?**
   - Browser shows website at http://localhost:8000/ ✅

3. **Database Connected?**
   - Create a survey → Check Compass → See data ✅

---

## 🔧 Common Commands

```powershell
# Activate virtual environment
.\env\Scripts\activate

# Start Django server
python manage.py runserver

# Stop server
CTRL + C

# Create admin user
python manage.py createsuperuser

# Run migrations
python manage.py migrate
```

---

## 🆘 Quick Fixes

**"MongoDB not found"**
→ Install MongoDB or start the service

**"Module not found"**
→ `pip install -r requirements.txt`

**"Port 8000 in use"**
→ `python manage.py runserver 8001`

**"Can't connect to MongoDB"**
→ Make sure `mongod` is running

