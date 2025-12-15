# What You Should See in MongoDB Compass

## Quick Answer

**You should see a database called `sondagesdb`** - but it will only appear **AFTER you successfully save a survey!**

If you don't see it yet, that's normal - MongoDB creates databases automatically when you first save data to them.

---

## Step-by-Step: What to Look For

### 1. Current Situation

Right now in MongoDB Compass, you're seeing:
- `admin` database (MongoDB system database)
- `config` database (MongoDB configuration)
- `local` database (MongoDB local data)

**This is normal!** These are MongoDB's system databases. Your application database (`sondagesdb`) doesn't exist yet because no data has been saved.

---

### 2. After Saving a Survey Successfully

Once you save a survey (after we fix the error), you'll see:

**New Database: `sondagesdb`**

Inside `sondagesdb`, you'll see these **Collections** (like tables):

1. **`sondages`** - Contains your surveys
   - Each document = one survey
   - Fields: title, description, user_id, created_at, etc.

2. **`questions`** - Contains all questions from all surveys
   - Each document = one question
   - Fields: text, question_type, sondage (link to survey), etc.

3. **`choices`** - Contains answer options for multiple choice questions
   - Each document = one choice option
   - Fields: text, question (link to question)

4. **`reponses`** - Contains survey submissions
   - Each document = one person's submission
   - Fields: sondage, user_id, ip_address, date, etc.

5. **`answers`** - Contains individual answers
   - Each document = one answer to one question
   - Fields: reponse (link to submission), question, texte, choix

---

## How to Verify Data is Saved

### Step 1: Save a Survey
1. Go to your website: http://localhost:8000/
2. Create a survey
3. Add questions
4. Save it

### Step 2: Check MongoDB Compass
1. **Refresh** MongoDB Compass (click the refresh button 🔄)
2. Look for **`sondagesdb`** in the database list
3. Click on **`sondagesdb`**
4. You should see collections listed:
   - `sondages` (at least 1 document)
   - `questions` (at least 1 document)
   - Possibly `choices` if you created choice questions

### Step 3: View Your Data
1. Click on **`sondages`** collection
2. You'll see documents (like rows) showing your surveys
3. Each document shows as JSON with fields like:
   ```json
   {
     "_id": ObjectId("693ee15a121c7341cf7dc831"),
     "title": "Your Survey Title",
     "description": "Your description",
     "user_id": 1,
     "created_at": ISODate("2025-12-14T...")
   }
   ```

---

## What Each Collection Contains

### Collection: `sondages`
**Purpose:** Stores survey information
**Example Document:**
```json
{
  "_id": ObjectId("693ee15a121c7341cf7dc831"),
  "title": "Customer Satisfaction Survey",
  "description": "Tell us about your experience",
  "user_id": 1,
  "created_at": ISODate("2025-12-14T17:30:00Z"),
  "shareable_link": UUID("a1b2c3d4-...")
}
```

### Collection: `questions`
**Purpose:** Stores all questions
**Example Document:**
```json
{
  "_id": ObjectId("693ee15a121c7341cf7dc832"),
  "sondage": ObjectId("693ee15a121c7341cf7dc831"),  // Links to survey
  "text": "How satisfied are you?",
  "question_type": "sc",  // Single choice
  "required": true
}
```

### Collection: `choices`
**Purpose:** Stores answer options (for multiple choice questions)
**Example Document:**
```json
{
  "_id": ObjectId("693ee15a121c7341cf7dc833"),
  "question": ObjectId("693ee15a121c7341cf7dc832"),  // Links to question
  "text": "Very Satisfied"
}
```

### Collection: `reponses`
**Purpose:** Stores survey submissions
**Example Document:**
```json
{
  "_id": ObjectId("693ee15a121c7341cf7dc834"),
  "sondage": ObjectId("693ee15a121c7341cf7dc831"),  // Which survey
  "user_id": 2,  // Who submitted
  "ip_address": "192.168.1.100",
  "date": ISODate("2025-12-14T18:00:00Z")
}
```

### Collection: `answers`
**Purpose:** Stores individual answers to questions
**Example Document:**
```json
{
  "_id": ObjectId("693ee15a121c7341cf7dc835"),
  "reponse": ObjectId("693ee15a121c7341cf7dc834"),  // Which submission
  "question": ObjectId("693ee15a121c7341cf7dc832"),  // Which question
  "texte": "Very Satisfied",  // Answer text
  "choix": []  // For choice questions, contains choice IDs
}
```

---

## Troubleshooting

### Q: I don't see `sondagesdb` database!
**A:** This means no survey has been saved yet. The database is created automatically when you save your first survey.

**To fix:**
1. Make sure the save error is fixed
2. Create and save a survey
3. Refresh MongoDB Compass
4. You should see `sondagesdb` appear

### Q: I see `sondagesdb` but it's empty (no collections)!
**A:** This shouldn't happen - collections are created when data is saved. If you see the database but no collections, try:
1. Refreshing MongoDB Compass
2. Checking if there were any errors when saving
3. Look in the Django terminal for error messages

### Q: I see collections but they're empty!
**A:** This means the survey save didn't complete successfully. Check:
1. Django terminal for errors
2. Make sure MongoDB is running
3. Try saving again

### Q: What if I still only see admin, config, local?
**A:** This means:
- Either no survey has been saved yet (normal if you haven't saved anything)
- OR the save failed with an error (check Django terminal)

---

## Summary

**What you should see RIGHT NOW:**
- admin, config, local databases (MongoDB system databases) ✅ This is normal!

**What you should see AFTER saving a survey:**
- `sondagesdb` database
- Inside it: `sondages`, `questions`, possibly `choices` collections
- Documents (data) inside each collection

**Remember:** MongoDB creates databases and collections automatically when you first save data. If `sondagesdb` doesn't exist yet, it's because no survey has been successfully saved!

