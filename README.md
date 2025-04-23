# 🤖 Telegram Bot for Paid Subscriptions

[![Aiogram](https://img.shields.io/badge/aiogram-3.13.1-blue)](https://github.com/aiogram/aiogram)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0.36-green)](https://www.sqlalchemy.org/)
[![APScheduler](https://img.shields.io/badge/APScheduler-3.10.4-orange)](https://github.com/agronholm/apscheduler)
[![Python](https://img.shields.io/badge/Python-3.11-yellow)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-lightgrey)](LICENSE)

A bot for managing paid subscriptions to private Telegram channels with a referral system and automated access control.


## 🚀 Installation and Launch

### Requirements

- Docker and Docker Compose
- Bot created via [@BotFather](https://t.me/BotFather)
- Private Telegram channel

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/bdpwm/paidsub-bot
   cd paidsub-bot
   ```

2. **Set up environment**
   ```bash
   cp .env.example .env
   # Edit .env with your data
   ```

3. **Build and run**
   ```bash
   docker-compose build
   docker-compose up -d
   ```

## ⚙️ Configuration

Edit your `.env` file with the following parameters:

```env
# Bot token from @BotFather
TOKEN='your_bot_token'

# PostgreSQL settings
POSTGRES_PASSWORD='secure_password'
POSTGRES_USER='username'
POSTGRES_DB='dbname'
POSTGRES_HOST='postgres'
POSTGRES_PORT='5432'

# Bot settings
ADMINS='123456789,987654321' # Admin IDs, comma-separated
CHANNEL_ID=-1001234567890    # Channel ID (with -100 prefix)
BOT_USERNAME='@your_bot'     # Bot username with @ symbol

# Subscription settings
SUBSCRIPTION_COST=100        # Subscription cost
SUBSCRIPTION_PERCENT=0.1     # Referral percentage (0.1 = 10%)
BONUS_DAYS=3                 # Bonus days for referrals
```

> 💡 **Tip:** You can find user and channel IDs using [@scanbitbot](https://t.me/scanbitbot)

## 🔐 Channel Setup

1. **Add the bot to your private channel as an administrator**

2. **Grant these permissions**:
   - ✅ Add users
   - ✅ Block users
   - ✅ Invite via link

3. **Verify permissions** with the `/admin_check_channel` command (as admin sure)


### P.S.
This bot is being continuously improved and updated as time permits, yep 0.o
