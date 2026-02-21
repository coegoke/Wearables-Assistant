# Wearables Assistant - Microservices Architecture

> A modern full-stack application for querying wearables data using AI, built with FastAPI, React, and LangGraph.

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green.svg)
![React](https://img.shields.io/badge/React-18.2-blue.svg)
![LangGraph](https://img.shields.io/badge/LangGraph-0.2-purple.svg)

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Prerequisites](#-prerequisites)
- [Features](#-features)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [Installation](#-installation)
- [Running the Application](#️-running-the-application)

---

## 🎯 Overview

Wearables Assistant is a conversational AI application that helps users query and analyze their wearable device data through natural language.

---

## ✅ Prerequisites

Before you begin, ensure you have the following installed:

| Software | Minimum Version | Recommended | Download |
|----------|----------------|-------------|----------|
| Python | 3.9+ | 3.11+ | [python.org](https://www.python.org/downloads/) |
| Node.js | 16.x+ | 20.x LTS | [nodejs.org](https://nodejs.org/) |
| npm | 8.x+ | 10.x+ | Included with Node.js |
| Git | 2.x+ | Latest | [git-scm.com](https://git-scm.com/) |

**Additional Requirements:**
- GROQ API Key (for LLM access) - Get it from [console.groq.com](https://console.groq.com)
- Terminal/Command Line access
- Code editor (VS Code recommended)

---

## ✨ Features

### Core Functionality
- 🤖 **AI-Powered Chat Interface** - Natural language queries for wearable data
- 📊 **Multi-Channel Support** - Organize conversations by topics
- 🔄 **Real-time Updates** - Live chat responses with streaming support
- 📈 **Data Visualization** - View agent workflow graphs

### Wearables Data Queries
- 👣 **Daily Steps Tracking** - Get step counts for specific dates or ranges
- 😴 **Sleep Analysis** - Total sleep, deep sleep, REM sleep, and sleep scores
- ❤️ **Heart Rate Monitoring** - Resting, average, max, and min heart rates
- 🏃 **Activity History** - Workout tracking with activity type filtering
- 📅 **Weekly Summaries** - Comprehensive weekly health reports
- 🔍 **Date Range Search** - Query data across custom date ranges
- 📱 **Device Information** - View connected wearable device details

### Technical Features
- 🎯 **LangGraph Agent** - Intelligent query routing and tool selection
- 🧠 **Groq LLM Integration** - Powered by Llama 3.3 70B model
- 💾 **SQLite Database** - Persistent chat and channel storage
- 🔌 **RESTful API** - Clean FastAPI backend architecture
- ⚡ **Fast Development** - Hot reload for both frontend and backend

---

## 🏗️ Architecture

### System Design

```text
┌─────────────┐         ┌──────────────┐         ┌────────────────┐
│   React     │◄───────►│   FastAPI    │◄───────►│   LangGraph    │
│   Frontend  │   HTTP  │   Backend    │         │     Agent      │
└─────────────┘         └──────────────┘         └────────────────┘
                                │                         │
                                ▼                         ▼
                        ┌──────────────┐         ┌────────────────┐
                        │   SQLite     │         │   Groq LLM     │
                        │   Database   │         │   (Llama 3.3)  │
                        └──────────────┘         └────────────────┘
```

---

## 🛠️ Tech Stack

### Backend

| Technology | Version | Purpose |
|------------|---------|---------|
| FastAPI | 0.104+ | Web framework |
| Uvicorn | 0.24+ | ASGI server |
| Pydantic | 2.5+ | Data validation |
| LangGraph | 0.2+ | Agent workflows |
| SQLite | 3.x | Database |

### Frontend

| Technology | Version | Purpose |
|------------|---------|---------|
| React | 18.2 | UI framework |
| Vite | 5.0 | Build tool |
| Axios | 1.6 | HTTP client |

---

## 🚀 Installation

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
```

### Frontend Setup

```bash
cd frontend
npm install
```

### Environment Setup

Create `.env` in root:

```bash
GROQ_API_KEY=your_groq_api_key_here
```

---

## ▶️ Running the Application

### Running Backend

1. Activate virtual environment:
```bash
cd backend
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows
```

2. Install dependencies (first time only):
```bash
pip install -r requirements.txt
```

3. Start the FastAPI server:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The backend will be available at: `http://localhost:8000`
- API documentation: `http://localhost:8000/docs`
- Alternative docs: `http://localhost:8000/redoc`

### Running Frontend

In a new terminal:

```bash
cd frontend
npm run dev
```

The frontend will be available at: `http://localhost:5173`

### Running Both Simultaneously

For development, open two terminal windows:

**Terminal 1 (Backend):**
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 (Frontend):**
```bash
cd frontend
npm run dev
```

---

