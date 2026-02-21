# Wearables Assistant - Microservices Architecture

> A modern full-stack application for querying wearables data using AI, built with FastAPI, React, and LangGraph.

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green.svg)
![React](https://img.shields.io/badge/React-18.2-blue.svg)
![LangGraph](https://img.shields.io/badge/LangGraph-0.2-purple.svg)

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Installation](#installation)

---

## 🎯 Overview

Wearables Assistant is a conversational AI application that helps users query and analyze their wearable device data through natural language. The application uses a microservices architecture with a FastAPI backend and React frontend, powered by LangGraph for intelligent agent workflows.

---

## 🏗️ Architecture

### System Design

\`\`\`
┌─────────────┐         ┌──────────────┐         ┌────────────────┐
│             │         │              │         │                │
│   React     │◄───────►│   FastAPI    │◄───────►│   LangGraph    │
│   Frontend  │   HTTP  │   Backend    │         │     Agent      │
│             │         │              │         │                │
└─────────────┘         └──────────────┘         └────────────────┘
                                │                         │
                                │                         │
                                ▼                         ▼
                        ┌──────────────┐         ┌────────────────┐
                        │              │         │                │
                        │   SQLite     │         │   Groq LLM     │
                        │   Database   │         │   (Llama 3.3)  │
                        │              │         │                │
                        └──────────────┘         └────────────────┘
\`\`\`

### Component Flow

1. **User Interface (React)**
   - Modern ChatGPT-like interface
   - Real-time message updates
   - Tool execution display
   - Channel management
   - Graph visualization sidebar

2. **API Layer (FastAPI)**
   - RESTful endpoints
   - CORS-enabled
   - Request/response validation
   - Error handling
   - OpenAPI documentation

3. **Business Logic (Services)**
   - Agent service (LangGraph management)
   - Channel service (conversation management)
   - Graph service (visualization)

4. **AI Agent (LangGraph)**
   - State machine workflow
   - Tool selection and execution
   - Conversation context management

5. **Data Layer (SQLite)**
   - User profiles
   - Device information
   - Health metrics
   - Activity data

---

## 🛠️ Tech Stack

### Backend

| Technology | Version | Purpose |
|------------|---------|---------|
| **FastAPI** | 0.104+ | Web framework |
| **Uvicorn** | 0.24+ | ASGI server |
| **Pydantic** | 2.5+ | Data validation |
| **LangGraph** | 0.2+ | Agent workflows |
| **LangChain** | 0.3+ | LLM framework |
| **Groq** | 0.11+ | LLM provider |
| **SQLite** | 3.x | Database |
| **Pillow** | 10.0+ | Image processing |

### Frontend

| Technology | Version | Purpose |
|------------|---------|---------|
| **React** | 18.2 | UI framework |
| **Vite** | 5.0 | Build tool |
| **Axios** | 1.6 | HTTP client |
| **React Markdown** | 9.0 | Markdown rendering |
| **Lucide React** | 0.294 | Icons |
| **Mermaid** | 10.6 | Diagram rendering |
| **date-fns** | 2.30 | Date formatting |

---

## 🚀 Installation

### Prerequisites

- **Python**: 3.10 or higher
- **Node.js**: 18.0 or higher
- **npm**: 9.0 or higher
- **Groq API Key**: Free at [console.groq.com](https://console.groq.com)

### Step 1: Backend Setup

\`\`\`bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# macOS/Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Return to root
cd ..
\`\`\`

### Step 2: Frontend Setup

\`\`\`bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Return to root
cd ..
\`\`\`

### Step 3: Environment Configuration

Create a `.env` file in the **root directory**:

\`\`\`bash
# Groq API Configuration
GROQ_API_KEY=gsk_your_groq_api_key_here

# Optional: LangSmith Configuration (for monitoring)
LANGSMITH_TRACING=true
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
LANGSMITH_API_KEY=lsv2_pt_your_langsmith_api_key_here
LANGSMITH_PROJECT=wearables
\`\`\`

**Get Groq API Key:**
1. Visit [console.groq.com](https://console.groq.com)
2. Create a free account
3. Generate API key
4. Copy to `.env` file

### Step 4: Database Initialization

\`\`\`bash
# Create sample database
python database.py
\`\`\`
