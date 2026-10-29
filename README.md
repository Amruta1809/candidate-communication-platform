# Candidate Communication Platform

A recruiter-facing candidate messaging platform. It has a Django REST API and a Next.js + TypeScript + Material UI dashboard.

## What is included

- Candidate creation, searching, listing, and details
- Individual and bulk messages, each tracked independently
- A simulated external provider with deterministic success, temporary failure, and invalid-recipient cases
- Provider-style status callbacks with idempotent, monotonic status handling
- Candidate communication history, failure reasons, and retry for retryable failures
- Provider health and live delivery statistics
- Message templates (bonus)

## Run locally

Requirements: Python 3.11+ and Node 20+.

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

In a second terminal:

```powershell
cd frontend
npm install
npm run dev
```

Open `http://localhost:3000`. The API runs at `http://localhost:8000/api`.

## Design notes and assumptions

The simulated provider is intentionally a separate adapter (`communications/provider.py`). Its returned external reference is stored on every message, and it sends a status update through the same webhook API a real provider would use. The `ProviderGateway` interface is the seam for Twilio/WhatsApp/Resend later.

Messages containing `invalid` (or candidates with malformed phone numbers) are permanent failures. Messages containing `temporary` fail once as retryable; all other messages progress Sent → Delivered → Read. In production, async provider work and callbacks would be queued and authenticated; the local simulator returns a status synchronously to make the assignment demonstrable.

Status updates are idempotent and never move a message backwards. No authentication is included because this is a single-recruiter assignment scope.

## Deployment

The repository includes a Render Blueprint in `render.yaml`. Create a new Render Blueprint from the GitHub repository. Render will provision PostgreSQL and deploy the Django API. Set `CORS_ALLOWED_ORIGINS` and `CSRF_TRUSTED_ORIGINS` to the deployed Vercel URL after creating the frontend deployment.

Import this repository into Vercel with `frontend` as the Root Directory. Add `NEXT_PUBLIC_API_URL` with the deployed API URL plus `/api` (for example, `https://candidate-connect-api.onrender.com/api`), then redeploy the frontend. Keep `DEBUG=False`, use the generated `SECRET_KEY`, and set `ALLOWED_HOSTS` to the Render API hostname in production.
