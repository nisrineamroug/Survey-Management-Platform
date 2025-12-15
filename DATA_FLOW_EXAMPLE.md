# Real Example: What Happens When Someone Submits a Survey

## Let's Trace a Complete Submission Step by Step

### Scenario:
1. User creates a survey: "Customer Satisfaction Survey"
2. Adds 2 questions:
   - Question 1: "Rate our service (1-5)" - Scale question
   - Question 2: "What did you like?" - Text question
3. Someone fills out and submits the survey

---

## Step 1: Survey Created

**In MongoDB Compass → `sondages` collection:**

```json
{
  "_id": ObjectId("65a1b2c3d4e5f6a7b8c9d0e1"),
  "title": "Customer Satisfaction Survey",
  "description": "Tell us about your experience",
  "user_id": 1,
  "created_at": ISODate("2024-01-15T10:00:00Z"),
  "shareable_link": UUID("a1b2c3d4-e5f6-7890-abcd-ef1234567890"),
  "primary_color": "#4F46E5",
  "background_color": "#ffffff",
  "limit_ip": true
}
```

**What you see in Compass:**
- Collection: `sondages`
- One document with survey details
- `_id` is the unique identifier (like primary key in SQL)

---

## Step 2: Questions Added

**In MongoDB Compass → `questions` collection:**

**Question 1:**
```json
{
  "_id": ObjectId("65a1b2c3d4e5f6a7b8c9d0e2"),
  "sondage": ObjectId("65a1b2c3d4e5f6a7b8c9d0e1"),  // ← Links to survey above
  "text": "Rate our service (1-5)",
  "question_type": "scal",
  "required": true,
  "min_value": 1,
  "max_value": 5
}
```

**Question 2:**
```json
{
  "_id": ObjectId("65a1b2c3d4e5f6a7b8c9d0e3"),
  "sondage": ObjectId("65a1b2c3d4e5f6a7b8c9d0e1"),  // ← Same survey
  "text": "What did you like?",
  "question_type": "tx",
  "required": true
}
```

**What you see in Compass:**
- Collection: `questions`
- Two documents
- Both have `sondage` field pointing to the survey's `_id`

---

## Step 3: Someone Submits the Survey

**Answers provided:**
- Question 1 (Scale): Selected "4"
- Question 2 (Text): "Great customer service!"

### 3a. A Reponse Document is Created

**In MongoDB Compass → `reponses` collection:**

```json
{
  "_id": ObjectId("65a1b2c3d4e5f6a7b8c9d0e4"),
  "sondage": ObjectId("65a1b2c3d4e5f6a7b8c9d0e1"),  // ← Which survey
  "user_id": 2,  // ← Who submitted (or null if anonymous)
  "ip_address": "192.168.1.100",
  "date": ISODate("2024-01-15T11:30:00Z"),
  "created_at": ISODate("2024-01-15T11:30:00Z"),
  "answer": ""
}
```

**What you see in Compass:**
- Collection: `reponses`
- One new document representing this submission
- Contains metadata (when, who, which survey)

---

### 3b. Answer Documents are Created (One per Question)

**In MongoDB Compass → `answers` collection:**

**Answer to Question 1:**
```json
{
  "_id": ObjectId("65a1b2c3d4e5f6a7b8c9d0e5"),
  "reponse": ObjectId("65a1b2c3d4e5f6a7b8c9d0e4"),  // ← Links to submission above
  "question": ObjectId("65a1b2c3d4e5f6a7b8c9d0e2"),  // ← Links to Question 1
  "texte": "4",  // ← The answer (scale 1-5)
  "choix": []  // ← Empty (only used for choice questions)
}
```

**Answer to Question 2:**
```json
{
  "_id": ObjectId("65a1b2c3d4e5f6a7b8c9d0e6"),
  "reponse": ObjectId("65a1b2c3d4e5f6a7b8c9d0e4"),  // ← Same submission
  "question": ObjectId("65a1b2c3d4e5f6a7b8c9d0e3"),  // ← Links to Question 2
  "texte": "Great customer service!",  // ← The text answer
  "choix": []  // ← Empty
}
```

**What you see in Compass:**
- Collection: `answers`
- Two documents (one for each question)
- Both link to the same `reponse` (submission)
- Each links to its specific `question`

---

## How to View This in MongoDB Compass

### Method 1: Browse All Collections

1. **Open MongoDB Compass**
2. **Connect to:** `mongodb://localhost:27017`
3. **Click on:** `sondagesdb`
4. **See 4 collections:**
   - `sondages` - Your surveys
   - `questions` - All questions
   - `reponses` - All submissions
   - `answers` - All individual answers

### Method 2: Filter to Find Specific Data

**Find all submissions for a specific survey:**

1. Go to `reponses` collection
2. Click "Filter" button (top right)
3. Enter filter:
   ```json
   {"sondage": ObjectId("65a1b2c3d4e5f6a7b8c9d0e1")}
   ```
4. Replace the ObjectId with your survey's actual `_id`
5. Click "Apply"

**Result:** You'll see only submissions for that survey!

---

**Find all answers for a specific submission:**

1. Go to `answers` collection
2. Click "Filter"
3. Enter:
   ```json
   {"reponse": ObjectId("65a1b2c3d4e5f6a7b8c9d0e4")}
   ```
4. Replace with your submission's `_id`

**Result:** You'll see all answers from that one submission!

---

## Understanding the Relationships

```
Sondage (Survey)
    ↓
    ├── Question 1
    │       ↓
    │       └── Answer (from Response 1)
    │       └── Answer (from Response 2)
    │       └── Answer (from Response 3)
    │
    └── Question 2
            ↓
            └── Answer (from Response 1)
            └── Answer (from Response 2)
            └── Answer (from Response 3)

Response 1
    ↓
    ├── Answer to Question 1
    └── Answer to Question 2
```

**In MongoDB:**
- Each box above is a separate document in its collection
- They're connected by ObjectId references (like foreign keys)
- MongoDB Compass shows these as ObjectIds (like `ObjectId("65a1b2...")`)

---

## Example with Multiple Choice Question

If Question 1 was "What did you like?" with choices:
- Option A: "Service"
- Option B: "Price"
- Option C: "Quality"

### In `choices` collection:

```json
{
  "_id": ObjectId("65a1b2c3d4e5f6a7b8c9d0e7"),
  "question": ObjectId("65a1b2c3d4e5f6a7b8c9d0e2"),
  "text": "Service"
}
```

```json
{
  "_id": ObjectId("65a1b2c3d4e5f6a7b8c9d0e8"),
  "question": ObjectId("65a1b2c3d4e5f6a7b8c9d0e2"),
  "text": "Price"
}
```

```json
{
  "_id": ObjectId("65a1b2c3d4e5f6a7b8c9d0e9"),
  "question": ObjectId("65a1b2c3d4e5f6a7b8c9d0e2"),
  "text": "Quality"
}
```

### If user selects "Service" and "Price", the Answer document:

```json
{
  "_id": ObjectId("65a1b2c3d4e5f6a7b8c9d0ea"),
  "reponse": ObjectId("65a1b2c3d4e5f6a7b8c9d0e4"),
  "question": ObjectId("65a1b2c3d4e5f6a7b8c9d0e2"),
  "texte": null,  // No text answer
  "choix": [
    ObjectId("65a1b2c3d4e5f6a7b8c9d0e7"),  // Service
    ObjectId("65a1b2c3d4e5f6a7b8c9d0e8")   // Price
  ]
}
```

**In MongoDB Compass:**
- The `choix` field shows an array of ObjectIds
- These are the selected choices
- Click on an ObjectId in Compass to see if it's clickable (some versions let you navigate)

---

## Quick Reference: Collection Purposes

| Collection | Contains | Purpose |
|-----------|----------|---------|
| `sondages` | Survey information | Title, description, settings, who created it |
| `questions` | All questions | Question text, type, settings (one per question) |
| `choices` | Answer options | For multiple choice questions (Option A, B, C, etc.) |
| `reponses` | Survey submissions | When someone submits a survey (one per submission) |
| `answers` | Individual answers | Answer to each question (one answer per question per submission) |

---

## Pro Tips for MongoDB Compass

1. **Search Bar:** Use the search at the top to quickly find text in documents

2. **Sort:** Click column headers to sort (like Excel)

3. **Export:** Click "Export Collection" to download data as JSON or CSV

4. **Indexes:** MongoDB automatically creates indexes on `_id` - don't worry about this for now

5. **Documents Tab vs Table View:**
   - Documents view: Shows full JSON (detailed)
   - Table view: Shows in spreadsheet format (easier to scan)

6. **Counting:** At the top of each collection, you'll see the total number of documents

---

## Troubleshooting

**Q: I don't see any data in Compass!**
- Make sure MongoDB is running
- Make sure you've run the Django app and created some surveys
- Check you're looking at the right database (`sondagesdb`)

**Q: I see ObjectIds everywhere - is that normal?**
- YES! ObjectIds are MongoDB's way of identifying documents
- They're like primary keys in SQL databases
- Each document has a unique `_id` field

**Q: How do I edit data in Compass?**
- Click on a document
- Click the pencil icon to edit
- Make changes and click "Update"
- ⚠️ Be careful! Editing directly can break relationships

**Q: Can I delete data in Compass?**
- Yes, but be careful!
- Deleting a survey might leave orphaned questions/answers
- It's safer to delete through your Django app

