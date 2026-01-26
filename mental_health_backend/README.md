# 🧠 Mental Health Agentic AI Backend

This module implements a **Level-1 Agentic AI backend** for mental health screening, crisis detection, and daily emotional check-ins.  
It is designed to be **safe, explainable, frontend-friendly**, and **easily integrable** into a larger backend system.

> ⚠️ This backend is **domain-specific** (mental health support).  
> It is intentionally **not a general chatbot**.

---

## ✨ What This Backend Does

### Core Capabilities
- Conversational mental health support
- Self-harm and crisis intent detection
- Risk classification with escalation actions
- Daily mental health check-ins
- Supportive advice generation
- Lightweight persistence (messages, risk events, summaries)

### AI Characteristics
- Uses a **real LLM** for reasoning and language understanding
- Constrained by **safety guardrails**
- Produces **structured JSON output** (not free text)
- Designed for **healthcare-safe behavior**

---

## 🧠 Agentic AI Design (High Level)

This backend follows a **Level-1 Agentic AI architecture**:

- **Single AI agent**
  - Interprets user input
  - Assesses emotional risk
  - Generates empathetic responses
  - Suggests next actions

- **Deterministic guardrails**
  - Intent-aware self-harm detection
  - Rule-based escalation logic
  - AI output is never blindly trusted

- **Explainable outputs**
  - Risk level
  - Self-harm flag
  - Recommended actions
  - Advice list

This mirrors how **real mental-health AI systems** are built in production.

---

## 📦 Response Contract (Important for Frontend)

All conversational responses follow this **stable JSON structure**:

```json
{
  "reply": "string (what the user sees)",
  "risk_level": "none | low | medium | high | critical",
  "self_harm_detected": true | false,
  "advice": ["string", "string"],
  "actions": ["ACTION_CODE"],
  "timestamp": "ISO-8601"
}

actions Field (Frontend-Driven UX)
The backend does not trigger UI changes directly.
Instead, it sends action hints that the frontend should interpret.

Action Code	Intended Frontend Behavior
NONE	Normal chat flow
SUGGEST_TRUSTED_CONTACT	Prompt user to reach out to someone
SHOW_HELPLINE	Display helpline information
SHOW_SOS	Show emergency/SOS UI
Frontend controls what to show, how, and when.

📝 Daily Check-in Concept
The backend supports a daily emotional check-in flow:
Frontend requests today’s questions
User answers short reflective prompts

Backend:
Summarizes emotional state
Assesses risk
Returns supportive guidance
This enables:
Mood tracking
Trend analysis
Preventive screening (before crisis)
🗄️ Persistence (Lightweight & Optional)
The backend stores:
User messages (user + AI)
Risk assessment events
Daily summaries

Purpose:
Conversation continuity (future enhancement)
Emotional trend analysis
Auditability for safety decisions
Storage is intentionally lightweight and replaceable.

🔐 Safety & Ethics Principles
This backend intentionally enforces boundaries:
❌ No medical diagnosis
❌ No medication advice
❌ No encouragement of harmful behavior
✅ Crisis detection and escalation
✅ Encouragement of real-world support
✅ Non-judgmental, calm tone
If a message indicates high or critical risk, the system:
Elevates severity
Suggests immediate support
Avoids casual or dismissive replies

🎨 Frontend Integration Guidelines
Chat UI
Treat responses as conversation turns
Do not assume conversation ends after one message
Allow users to continue typing naturally
Risk-Aware UI
Use risk_level + actions to guide UX
Avoid alarming UI for low/medium risk
Be clear and supportive for high/critical risk
Recommended UX Patterns
Soft prompts: “Do you want to talk more?”
Non-blocking suggestions
Clear but calm escalation visuals

🚀 Extensibility (Future-Ready)
This backend is designed to evolve into:
Multi-agent architecture (separate risk, memory, and response agents)
Short-term conversational memory
Long-term emotional insights
Personalization (with consent)
The current design keeps these upgrades safe and non-breaking.

🧪 Testing Philosophy
APIs are fully testable via interactive documentation
Structured responses make frontend mocking easy
Safety scenarios are deterministic and reproducible

🧩 Intended Usage
This module is meant to be:
Integrated into a larger backend system
Consumed by mobile or web frontends
Used as a support tool, not a replacement for professionals

📌 Final Note
This is not a toy chatbot.

It is a domain-constrained, safety-first AI system built with:
Real reasoning
Clear intent detection
Professional guardrails
Exactly how responsible AI systems are expected to work.