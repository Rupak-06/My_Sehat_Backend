# My_Sehat_Backend

My_Sehat_Backend is the unified backend service for the **MySehat** healthcare platform.
It brings together multiple independent FastAPI-based healthcare modules into a single
gateway server while preserving clear separation of concerns.

## 🚀 Features

- Single FastAPI gateway
- One port / one domain
- Unified Swagger UI
- Modular architecture
- Easy to extend with new backend modules
- No duplication of business logic

## 🧩 Backend Modules

The backend consists of the following independent modules:

1. **Diagnostics AI Triage**
   - Symptom-based triage (text / image)
   - Session-based follow-up questions
   - Severity and urgency classification

2. **Mental Health AI Triage**
   - AI-powered mental health chat
   - Crisis and risk detection
   - User-level conversation handling

3. **Medicine Reminder**
   - Medicine scheduling
   - Reminder management
   - Prescription-based workflows

Each module is developed independently and composed at runtime by the gateway.

## 🏗️ Architecture Overview

BACKEND/
│
├── diagnostics_backend/
│ └── main.py
│
├── mental_health_backend/
│ └── main.py
│
├── medicine_backend/
│ └── main.py
│
└── gateway/
└── main.py


- The `gateway` acts as the single entry point.
- Each backend module is mounted under its own route prefix.
- All APIs are exposed via a unified Swagger UI.

## 🌐 API Access

After starting the server:

- Unified Swagger UI:  
  `http://localhost:8000/docs`

- Module prefixes:
  - `/diagnostics/*`
  - `/mental-health/*`
  - `/medicine-reminder/*`

## ▶️ How to Run

### 1. Activate virtual environment
```bash
.venv\Scripts\activate   # Windows
# or
source .venv/bin/activate  # macOS/Linux
