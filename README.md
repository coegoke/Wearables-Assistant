# Wearables Assistant - Microservices Architecture

> A modern full-stack application for querying wearables data using AI, built with FastAPI, React, and LangGraph.

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green.svg)
![React](https://img.shields.io/badge/React-18.2-blue.svg)
![LangGraph](https://img.shields.io/badge/LangGraph-0.2-purple.svg)

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [Installation](#-installation)

---

## 🎯 Overview

Wearables Assistant is a conversational AI application that helps users query and analyze their wearable device data through natural language.

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

