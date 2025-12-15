# How to Check Answers in MongoDB Compass

## You Should See These Collections

After someone submits a survey, you should see **5 collections** in the `sondagesdb` database:

1. ✅ **`sondages`** - Your surveys (you can see this)
2. ✅ **`questions`** - Questions (you can see this)
3. **`choices`** - Answer options for multiple choice questions
4. **`reponses`** - Survey submissions (when someone fills out a survey)
5. **`answers`** - Individual answers to each question ⚠️ **This is what you're looking for!**

---

## Step-by-Step: Finding Answers

### Step 1: Open MongoDB Compass
- Make sure you're connected to `mongodb://localhost:27017`
- Click on **`sondagesdb`** database

### Step 2: Look for the `answers` Collection
- You should see **`answers`** in the collection list
- Click on **`answers`** collection

### Step 3: What You Should See

If someone has submitted a survey, you should see documents like this:

```json
{
  "_id": ObjectId("..."),
  "reponse": ObjectId("..."),  // Links to a submission in 'reponses'
  "question": ObjectId("..."),  // Links to a question in 'questions'
  "texte": "Answer text here",  // The answer (for text/scale questions)
  "choix": [                     // Selected choices (for choice questions)
    ObjectId("...")
  ]
}
```

---

## Troubleshooting: No Answers Showing?

### Check 1: Did Someone Actually Submit the Survey?

1. Check the **`reponses`** collection
2. If it's empty, no one has submitted a survey yet
3. Submit a test survey from your website first

### Check 2: Are Answers Being Saved?

After submitting a survey, check the Django terminal. You should see:
- No error messages
- The survey submission redirects to "merci" (thank you) page

### Check 3: Filter to Find Answers for a Specific Survey

1. Go to **`answers`** collection
2. Click **"Filter"** button (top right)
3. To find answers for a specific survey submission:
   - First, go to `reponses` collection
   - Find the submission's `_id`
   - Go back to `answers` collection
   - Enter filter: `{"reponse": ObjectId("paste_id_here")}`

### Check 4: Check for Errors

If answers aren't appearing, check:
1. Django terminal for error messages
2. Try submitting the survey again
3. Check that all questions are being answered in the form

---

## Understanding the Data Structure

### Example: Someone Fills Out a Survey

**1. Submission Created** (`reponses` collection):
```json
{
  "_id": ObjectId("abc123"),
  "sondage": ObjectId("survey_id"),
  "date": ISODate("2025-12-14T...")
}
```

**2. Answers Created** (`answers` collection - ONE per question):

**Answer 1:**
```json
{
  "_id": ObjectId("def456"),
  "reponse": ObjectId("abc123"),  // Links to submission above
  "question": ObjectId("q1_id"),  // Question 1
  "texte": "Very satisfied",      // Their answer
  "choix": []                     // Empty (not a choice question)
}
```

**Answer 2:**
```json
{
  "_id": ObjectId("ghi789"),
  "reponse": ObjectId("abc123"),  // Same submission
  "question": ObjectId("q2_id"),  // Question 2
  "texte": null,                  // No text (it's a choice question)
  "choix": [                      // Selected choices
    ObjectId("choice1_id")
  ]
}
```

---

## Quick Test

1. **Submit a test survey:**
   - Go to your website
   - Fill out and submit a survey

2. **Check MongoDB Compass:**
   - Refresh Compass
   - Go to `sondagesdb` → `answers`
   - You should see at least one document per question in the survey

3. **If still no answers:**
   - Check Django terminal for errors
   - Make sure you're looking at the `answers` collection (not `reponses`)
   - Try submitting again

---

## Collections Overview

| Collection | Contains | When Created |
|-----------|----------|--------------|
| `sondages` | Surveys | When you create a survey |
| `questions` | Questions | When you add questions to a survey |
| `choices` | Answer options | When you create multiple choice questions |
| `reponses` | Submissions | When someone submits a survey (1 per submission) |
| `answers` | Answers | When someone submits (1 per question per submission) |

**Important:** Answers are in the `answers` collection, NOT in `reponses`!

