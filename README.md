# ReqMind AI

AI-powered software requirements & test engineering platform (prototype).

This repository contains a full-stack prototype built with React (Vite) frontend and FastAPI backend. It includes authentication, project management, document upload stubs, an AI service abstraction (with a development/mock provider), and basic database models.

See `backend/.env.example` and `frontend/.env.example` for environment variables.

## Local quickstart

Backend:

```
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Frontend:

```
cd frontend
npm install
npm run dev
```
