# Telegram Bot for Paid Subscriptions to Private Telegram Channels

```
This project demonstrates a simple Telegram bot on aiogram 3.13.1 framework with PostgreSQL database integration via SQLAlchemy 2.0.36 library and task scheduling via APScheduler 3.10.4 library.

```



## Usage

To install requirements run the following command:

``` bash
pip install -r requirements.txt
```

Create an .env file in the root of the project and add the following variables to it:

``` textmate
TOKEN='bot_token'
ADMINS='00000000, 00000000'
ROOT_PASS='dasfg531KKK331xklaS'
PG_LINK='postgresql://username:password@host:port/dbname'
CHANNEL_ID=-10101010101
BOT_USERNAME='bot_username'
``` 

Replace the data with your own.

## Launch bot

``` bash
python aiogram_run.py
``` 