# Oracle Cloud Always Free deployment

This repo is ready to run on an Oracle Cloud Linux VM as a long-running bot process.

As of April 15, 2026, Oracle's official Free Tier page says Always Free includes compute options such as:

- AMD-based Compute
- Arm-based Ampere A1 Compute

Official sources:

- https://www.oracle.com/cloud/free/
- https://docs.oracle.com/iaas/Content/Compute/Tasks/instances.htm
- https://docs.oracle.com/iaas/Content/Compute/Tasks/accessinginstance.htm

## What was added

- `deploy/epn-bot.service`: a `systemd` service template to keep the bot running
- `.env.example`: environment variable template

## Recommended VM choice

If available in your region, choose Ubuntu 22.04 LTS or Oracle Linux.

This guide assumes:

- OS user is `ubuntu`
- app path is `/home/ubuntu/epn-discord-bot-main`

If you choose Oracle Linux, the default SSH user is often `opc`, so update the service file paths accordingly.

## Step 1: Create the instance in Oracle Cloud

1. Sign in to Oracle Cloud.
2. Open `Compute` -> `Instances`.
3. Click `Create instance`.
4. Choose an Always Free eligible shape.
5. Choose an Ubuntu or Oracle Linux image.
6. Assign a public IP so you can SSH in.
7. Paste your SSH public key during setup.
8. Create the instance and wait for it to reach `Running`.

## Step 2: Connect with SSH

Oracle's docs show SSH access in this form:

```bash
ssh -i /path/to/private_key ubuntu@YOUR_PUBLIC_IP
```

If you use Oracle Linux instead of Ubuntu, try:

```bash
ssh -i /path/to/private_key opc@YOUR_PUBLIC_IP
```

## Step 3: Install system packages

On Ubuntu:

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip git
```

On Oracle Linux, use the equivalent package manager commands.

## Step 4: Clone the repo

```bash
git clone https://github.com/YOUR_USERNAME/epn-discord-bot-main.git
cd epn-discord-bot-main
```

## Step 5: Create the virtual environment

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## Step 6: Create the environment file

Copy `.env.example` to `.env` and fill in at least:

- `TOKEN`
- `BOT_OWNER_ID`
- `DATABASE_URL`

Example:

```bash
cp .env.example .env
nano .env
```

Use PostgreSQL for production. If you already have Neon, its connection string can go into `DATABASE_URL`.

## Step 7: Test the bot manually

Before making it a service, start it once manually:

```bash
. .venv/bin/activate
python main.py
```

If it starts correctly, you should see log lines showing database connection success and the bot logging in.

Press `Ctrl+C` after confirming it works.

## Step 8: Install the systemd service

Copy the service file:

```bash
sudo cp deploy/epn-bot.service /etc/systemd/system/epn-bot.service
```

If your Linux username or app path is different, edit the service first:

```bash
sudo nano /etc/systemd/system/epn-bot.service
```

Make sure these match your server:

- `User=ubuntu`
- `WorkingDirectory=/home/ubuntu/epn-discord-bot-main`
- `EnvironmentFile=/home/ubuntu/epn-discord-bot-main/.env`
- `ExecStart=/home/ubuntu/epn-discord-bot-main/.venv/bin/python main.py`

Then enable and start it:

```bash
sudo systemctl daemon-reload
sudo systemctl enable epn-bot
sudo systemctl start epn-bot
```

## Step 9: Check logs

```bash
sudo systemctl status epn-bot
journalctl -u epn-bot -f
```

You want to see successful startup and no repeated crash loop.

## Discord checklist

In the Discord Developer Portal, enable these privileged intents because this bot requests them:

- Server Members Intent
- Message Content Intent
- Presence Intent

## Notes

- This bot does not need port `80` or `443` open because it is not a web app.
- The VM firewall can stay minimal if you only need SSH.
- Oracle capacity for Always Free can be limited by region. If one shape is unavailable, try another Always Free eligible shape or another home region.
