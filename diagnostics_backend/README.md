🩺 MySehat – AI-Powered Diagnostic Triage Backend
Improving Health Through Accessible and Empowering Innovation
MySehat is an AI-driven, offline-friendly healthcare platform designed to provide early diagnostic guidance, mental health support, and emergency assistance through a single unified application.
This repository contains the Diagnostic Triage Backend, which powers symptom-based and image-based health analysis with multi-turn conversational intelligence.

📌 What This Backend Does (In Simple Terms)
This backend acts like an AI health assistant that:
Understands user symptoms (text)
Analyzes uploaded medical images (skin, wounds, rashes, etc.)
Asks follow-up questions when needed
Maintains a conversation session
Produces a final structured health guidance response
⚠️ This is not a medical diagnosis — it is an early guidance & triage system.

🧠 Core Features
1. Symptom-Based AI Triage (Text)
Accepts user symptoms as plain English
Dynamically asks clarifying questions
Adjusts questions based on symptom category (systemic, GI, skin, neuro, etc.)
Ends with a structured guidance output

2. Image-Based AI Triage
Accepts medical images (skin, wounds, rashes)
Extracts visual features (redness, swelling, lesions, etc.)
Generates probable causes with confidence scores
Supports multi-image analysis within the same session

3. Multi-Turn Conversation Support
Every interaction belongs to a session
Backend remembers previous answers
Conversation continues until enough information is collected

4. Frontend-Friendly Structured Output
Responses are predictable JSON
Easy to render in Flutter / React
Designed for chat-style UI

🏗️ High-Level Architecture
Frontend (Flutter / Web)
        |
        |  REST APIs (JSON / multipart)
        v
FastAPI Backend
        |
        |-- Text Triage Engine
        |-- Image Analysis Engine
        |-- Question Flow Controller
        |-- Session Manager
        |
   Final Health Guidance Output

🔁 Understanding the Conversation Flow (IMPORTANT)
This is a 2-way conversational system, not a single request–response API.

Step 1: User Starts Conversation
User sends initial symptoms or uploads an image.
POST /api/v1/triage/text
or
POST /api/v1/triage/image

Step 2: Backend Responds
There are two possible states:
🟡 Needs More Information
{
  "session_id": "uuid",
  "status": "needs_more_info",
  "next_question": {
    "id": "q_systemic_1",
    "text": "How high is your fever and how long has it lasted?",
    "options": ["Low grade", "High grade", "No fever"],
    "allow_custom": true
  },
  "final_output": null
}
➡️ Frontend must now ask this question to the user

🟢 Completed
{
  "session_id": "uuid",
  "status": "completed",
  "next_question": null,
  "final_output": {
    "summary": "...",
    "severity": "low",
    "possible_causes": [...],
    "home_care": [...],
    "prevention": [...],
    "red_flags": [...],
    "when_to_seek_care": [...],
    "disclaimer": "..."
  }
}
➡️ Conversation can end or optionally continue

🔄 How to Continue the Conversation (Beginner Friendly)
When the backend asks a question:
Frontend should:
Store session_id
Show next_question.text
Collect user’s answer
Send it back with the same session_id

Example:
POST /api/v1/triage/text
{
  "session_id": "uuid",
  "answer": "No fever"
}

✅ This allows:
Context awareness
Correct follow-up logic
Higher confidence final result

🖼️ Multi-Image Conversation (Supported)
Yes — this is possible and recommended ✅

How it works:
First image creates a session
Second image is uploaded with the same session_id
Backend compares:
Findings from image 1
Findings from image 2
Produces a better, higher-confidence result

Frontend UX Example:
“Would you like to upload another image or ask a follow-up question?”

🔌 API Endpoints
1️⃣ Text Triage
POST /api/v1/triage/text
Content-Type: application/json

Initial Request:
{
  "symptoms": "I feel nauseous",
  "age": 22,
  "duration": "2 days",
  "severity": "low"
}

Follow-Up Request:
{
  "session_id": "uuid",
  "answer": "No fever"
}

2️⃣ Image Triage
POST /api/v1/triage/image
Content-Type: multipart/form-data

-F file=@image.jpg

Optional:
-F session_id=uuid

🎨 Frontend Integration Guide

UI Components Needed
Chat message list
Question card (options + free text)
Image upload button
Loading indicator
Result summary screen

State Management (Simple)
sessionId
conversationMessages[]
currentQuestion
finalResult

Logic
IF status == needs_more_info
  → show question
ELSE
  → show final result
  → ask "Do you want to continue?"

🛡️ Important Notes
This system does not diagnose
Always show disclaimer in UI
Encourage professional consultation for red flags
Designed for hackathon demo + real-world scalability

🚀 Why This Impresses Judges
✅ Multi-turn AI conversation (not static)
✅ Session-aware reasoning
✅ Image + text fusion
✅ Clean architecture
✅ Real healthcare workflow simulation
✅ Beginner-friendly yet production-ready