# Automatic Question Paper Generator

A full-stack application that helps faculty generate university examination question papers from uploaded syllabus and reference materials.

- Backend: FastAPI + SQLAlchemy + MySQL
- Frontend: React 19 + Vite
- LLM providers: OpenAI or Gemini (configurable)

## Features

- Secure authentication (signup/login with JWT)
- Upload syllabus and reference materials
- Generate multiple distinct question paper sets using Bloom's taxonomy
- View previously generated papers

## Tech Stack

- Backend: `fastapi`, `sqlalchemy`, `pymysql`, `python-jose`, `passlib`, `python-dotenv`
- Frontend: `react`, `react-router-dom`, `axios`, `vite`
- LLM: `openai` or `google-generativeai`

## Directory Structure

- `backend/` — FastAPI project (ASGI app at `app.main:app`)
- `frontend/` — React app (Vite dev server)

## Prerequisites

- Node.js 18+
- Python 3.10+
- MySQL 8+ running locally (or accessible remotely)

## Configuration

Create an `.env` file in `backend/` (a sample already exists). Common variables:

```
DB_USER=root
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=3306
DB_NAME=question_paper_db

JWT_SECRET_KEY=CHANGE_ME
ACCESS_TOKEN_EXPIRE_MINUTES=1440

LLM_PROVIDER=openai
OPENAI_API_KEY=sk-your-openai-key
GEMINI_API_KEY=your-gemini-key

FILE_UPLOAD_DIR=uploaded_files
```

Notes:
- The database must exist; tables are auto-created on app startup (`backend/app/main.py:8`).
- CORS dev origins are configured in `backend/app/main.py:12`.

## Backend Setup

1) Install dependencies:

```
cd backend
python -m pip install -r requirements.txt
```

2) Ensure MySQL database exists:

```
# Example (MySQL shell)
CREATE DATABASE question_paper_db;
```

3) Run the API server:

```
python -m uvicorn app.main:app --reload --port 8000
```

- API root: `http://127.0.0.1:8000/`
- Docs: `http://127.0.0.1:8000/docs`

## Frontend Setup

1) Install dependencies:

```
cd frontend
npm install
```

2) Run the dev server:

```
npm run dev
```

- App: `http://localhost:5173/`
- The frontend calls the backend at `http://localhost:8000` (`frontend/src/api.js:3`). If you change ports or host, update that base URL.

## Running Both (Dev)

- Terminal A:

```
cd backend
python -m uvicorn app.main:app --reload --port 8000
```

- Terminal B:

```
cd frontend
npm run dev
```

## API Reference

- Auth — signup/login (`backend/app/routers/auth_routes.py:12`, `backend/app/routers/auth_routes.py:33`)
  - POST `/auth/signup`
  - POST `/auth/login` → returns `access_token`

- User — profile (`backend/app/routers/user_routes.py:10`, `backend/app/routers/user_routes.py:26`)
  - GET `/user/me`
  - GET `/user/profile`
  - PUT `/user/profile`

- Files — uploads (`backend/app/routers/file_routes.py:23`, `backend/app/routers/file_routes.py:52`)
  - POST `/files/upload-syllabus` (multipart)
  - POST `/files/upload-reference` (multipart; `material_type` can be `reference` or `question_paper`)

- Papers — generation and retrieval (`backend/app/routers/paper_routes.py:13`, `backend/app/routers/paper_routes.py:137`, `backend/app/routers/paper_routes.py:151`)
  - POST `/papers/generate`
  - GET `/papers/`
  - GET `/papers/{paper_id}`

## LLM Configuration

- Choose provider via `LLM_PROVIDER` env: `openai` or `gemini` (`backend/app/config.py:21`).
- OpenAI errors are normalized (`backend/app/llm_service.py:48`). Gemini errors are normalized (`backend/app/llm_service.py:80`).

## Development

- Frontend lint: `npm run lint` (rules in `frontend/eslint.config.js`)
- JWT token added to requests via interceptor (`frontend/src/api.js:6`).

## Troubleshooting

- DB connection issues: verify `.env` and that MySQL is reachable (`backend/app/config.py:14`).
- CORS errors: adjust `origins` in `backend/app/main.py:12`.
- LLM quota or key errors: provider exceptions surface as HTTP 5xx/4xx from `llm_service`.

## Contributing

- Fork the repository and create a feature branch from `main`.
- Set up both apps locally and ensure you can run:
  - Backend: `python -m uvicorn app.main:app --reload --port 8000`
  - Frontend: `npm run dev`
- Follow existing patterns and code style used in the project.
- Frontend: run `npm run lint` and fix any issues before pushing.
- Avoid committing secrets; use environment variables via `.env`.
- Write clear commit messages and open a pull request describing the change.
- Link to any related issue and include testing steps in the PR description.

## License

This project is licensed under the MIT License. You are free to use, copy, modify,
merge, publish, distribute, sublicense, and/or sell copies of the software,
subject to the following permission notice and disclaimer:

```
MIT License

Copyright (c) 2025

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

