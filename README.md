# Klopotenko Telegram Bot 👨‍🍳🇺🇦
A Telegram bot that brings the culinary world of Yevhen Klopotenko—one of Ukraine's most famous chefs—directly to your chat. This bot helps users discover authentic and modern Ukrainian recipes, improve their cooking skills, and explore the "Cult Food" philosophy.

_Note: This project is an independent fan-made tool and is not officially affiliated with Yevhen Klopotenko's brand._

# 🌟 Features

+ Recipe Search: Find recipes by name or ingredients.
+ AI-Powered Assistance: Integration with LLMs (OpenAI) to answer cooking questions or suggest menu pairings in Klopotenko's signature style.
+ Ukrainian Culinary Heritage: Focused on reviving and modernizing traditional Ukrainian dishes (like authentic Borscht).
+ Interactive UX: Easy-to-use Telegram interface with buttons and intuitive commands.

# 🛠 Tech Stack
+ Language: Python 3.10+
+ Framework: pyTelegramBotAPI (Telebot)
+ AI Integration: Google AI API (for recipe suggestions and conversational AI)
+ Data: Scraped or integrated recipe database from Klopotenko's official resources.

# 🚀 Getting Started

## Prerequisites
The following is required to run this bot:
+ Python 3.x installed.
+ A Telegram Bot Token (from @BotFather).
+ An Google AI Studio API Key.

## Installation

Clone the repository:
```sh
git clone https://github.com/stupidcucumber/klopotenko-bot.git
cd klopotenko-bot
```

Install dependencies:
```sh
pip install -r requirements.txt
Environment Setup:
```

Create a .env file in the root directory and add your credentials using .env example file. And run the bot:
```sh
python bot.py
```

# 📖 Usage
Open Telegram and search for your bot.

Press `/start` to see the main menu.

Use commands like `/recipe` or simply type an ingredient (e.g., "beetroot") to get suggestions.

# 🏗 Project Structure
Plaintext
├── bot.py             # Main entry point for the bot
├── config.py          # Configuration and environment variables
├── handlers/          # Message and command handlers
├── utils/             # Helper functions and API wrappers
└── requirements.txt   # Project dependencies

# 👨‍💻 Author
Ihor Kostiuk - Machine Learning Engineer

GitHub: @stupidcucumber

📄 License
This project is licensed under the MIT License - see the LICENSE file for details.