# TG-bot-CS_FK

## About the attachment

A bot created to introduce children, schoolchildren or students, to computer technology.
In particular, the functionality of the presented application will be continuously expanded
and will provide more and more new and different features for interactivity
and immersion in the world of computer technology.

## Opportunities

Several functions are available:
Convert any words or letters, as well as symbols, into machine code as modern computers read it.
Also, reverse conversion, from machine code to human-readable characters or words.

## Others

The bot is developed using the aiogram framework, which makes it easy to create and manage bots for Telegram.

To run the bot, you need to install the dependencies specified in the requirements.txt file and configure the Telegram API token.
Detailed instructions on installation and configuration can be found below.

## Installation

Clone the TG-bot-CS_FK repository to your local machine.

```bash
git clone https://github.com/Aleks-Ti/TG-bot-CS_FK.git
```

Create and activate a virtual environment:

```bash
python3 -m venv venv
```

Activate virtual environment:

```bash
source venv/Sourse/activate (windows) / source venv/bin/activate (unix)
```

Install dependencies from the file requirements.txt:

```bash
pip install -r requirements.txt
```

## Перед запуском

```bash
cd projectС/
```

For the bot to work, you need to create a file in the .env folder and specify two keys:

Telegram bot token (required!)
Account id (optionally(not necessarily))

```bash
TOKEN = "your TG token of the channel bot"
CHAT_ID = 0123456789  # your personal ID (optionally)
```

### Start

```bash
cd projectС/
```

```bash
python main.py
```

### License

TG_bot-Exchange-rate is released under the MIT License.
