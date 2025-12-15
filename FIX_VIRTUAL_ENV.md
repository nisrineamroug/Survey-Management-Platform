# Fix Virtual Environment Error

## Problem
The virtual environment was created in a different location and is trying to use an old Python path that doesn't exist.

## Solution: Recreate the Virtual Environment

### Step 1: Delete the Old Virtual Environment

```powershell
# Make sure you're in the project folder
cd "C:\Users\halas\OneDrive\Bureau\sondage big data\sondageapp"

# Delete the old env folder
Remove-Item -Recurse -Force .\env
```

**OR manually:**
- Go to your project folder
- Delete the `env` folder completely

### Step 2: Create a New Virtual Environment

```powershell
# Still in the project folder
python -m venv env
```

### Step 3: Activate the New Virtual Environment

```powershell
.\env\Scripts\activate
```

You should see `(env)` at the beginning of your prompt.

### Step 4: Upgrade pip (Recommended)

```powershell
python -m pip install --upgrade pip
```

### Step 5: Install Requirements

```powershell
pip install -r requirements.txt
```

---

## Alternative: Install Packages Manually

If `requirements.txt` still has issues, install packages one by one:

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

## Verify It Works

After installation, test:

```powershell
python manage.py --version
```

You should see Django version.

