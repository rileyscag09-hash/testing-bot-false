# Koyeb deployment

As of April 15, 2026, Koyeb's official docs say:

- Koyeb supports `Worker` services for background jobs.
- Koyeb offers a `free` instance tier with 512 MB RAM, 0.1 vCPU, and 2 GB SSD.

Official docs:

- https://www.koyeb.com/docs/reference/services
- https://www.koyeb.com/docs/

This bot should be deployed to Koyeb as a `Worker`, not a web service.

## Files added for Koyeb

- `Procfile` with `worker: python main.py`
- `.env.example` already contains the variables you may need

## What you need to do

1. Push this repo to GitHub.
2. Create a Koyeb account.
3. In Koyeb, create a new App from your GitHub repo.
4. Choose the service type `Worker`.
5. If Koyeb asks for runtime/build details, use:

- Runtime: `Python`
- Build command: `pip install -r requirements.txt`
- Run command: `python main.py`

6. Choose the free instance type if it is offered in the UI.
7. Add these environment variables:

Required:

- `TOKEN`
- `BOT_OWNER_ID`

Strongly recommended:

- `DATABASE_URL`

Optional:

- `SENTRY_DSN`
- `OPENAI_API_KEY`
- `BLOXLINK_API_KEY`
- `WEB_RISK_API_KEY`
- `MELONLY_API_KEY`
- `OPENROUTER_API_KEY`
- `TWILIO_ACCOUNT_SID`
- `TWILIO_AUTH_TOKEN`
- `TWILIO_PHONE_NUMBER`
- `TWILIO_VERIFY_SERVICE_SID`
- `TWILIO_DEBUG_MODE`

## Database

Use PostgreSQL for production.

This repo now supports:

- `DATABASE_URL`
- `NEONDB_PROD`

If you already have a Neon database, you can paste that connection string into `DATABASE_URL` on Koyeb.

## Discord settings

In the Discord Developer Portal, enable:

- Server Members Intent
- Message Content Intent
- Presence Intent

## What to look for in logs

When the bot starts correctly, logs should show messages similar to:

- `Database connected successfully`
- `Logged in as ...`

## Notes

- The `package.json` in this repo is not the app you are deploying. This bot runs with Python.
- If Koyeb's UI auto-detects the wrong runtime because of `package.json`, manually set the service to Python and use the commands above.
- I am inferring that the free instance can be used for a small worker because Koyeb's docs currently say free instances are available and workers are a supported service type. If the Koyeb UI blocks free workers on your account, the fallback is Oracle Cloud Always Free or another host.
