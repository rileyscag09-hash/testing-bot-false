# Render deployment

This bot is best deployed on Render as a **Background Worker**, but a minimal healthcheck web server has also been added so it can run as a **Web Service** if you need the free plan workaround.

## What was added

- `render.yaml` so Render knows how to build and start the bot
- `runtime.txt` to pin Python
- `.env.example` with the environment variables you may need
- Support for Render's standard `DATABASE_URL` env var
- A tiny HTTP healthcheck server on `/` and `/health`

## Recommended Render setup

1. Push this project to GitHub.
2. In Render, create a **PostgreSQL** database.
3. In Render, create a new service from this repo using **Blueprint** or manually create a **Web Service** if you need free hosting.
4. If you use the blueprint, update `render.yaml` or create the web service manually in the dashboard because the checked-in blueprint is still set to `worker`.
5. Set these environment variables on the service:

Required:
- `TOKEN`
- `BOT_OWNER_ID`

Strongly recommended:
- `DATABASE_URL`

Needed for the web-service workaround:
- `PORT` with Render's injected value, or leave the host default behavior alone and let Render provide it automatically

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

## Important notes

- A tiny HTTP server has been added so Render/Replit can detect an open port.
- Do **not** rely on SQLite on Render for production. Render instances are ephemeral, so use PostgreSQL via `DATABASE_URL`.
- The repo contains a `package.json`, but this bot actually runs with Python. `render.yaml` makes Render use Python anyway.
- Free web services can still sleep after inactivity, so this workaround is not fully reliable for a Discord bot.

## Manual settings if you do not use Blueprint

- Environment: `Python`
- Build command: `pip install -r requirements.txt`
- Start command: `python main.py`
- Service type: `Web Service` for the free-tier workaround

## After deploy

Once the worker is live, check the Render logs for:

- `Database connected successfully`
- `Logged in as ...`
- `Healthcheck server listening on 0.0.0.0:PORT`

If startup fails, it is usually one of these:

- missing `TOKEN`
- invalid `BOT_OWNER_ID`
- missing or invalid `DATABASE_URL`
- Discord privileged intents not enabled in the Discord Developer Portal

## Discord portal checklist

In the Discord Developer Portal for your bot, make sure these privileged intents are enabled because the bot requests them:

- Server Members Intent
- Message Content Intent
- Presence Intent
