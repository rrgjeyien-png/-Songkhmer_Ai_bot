import os
import asyncio
import threading
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from openai import OpenAI

# ១. បង្កើត Web Server ការពារកុំឱ្យ Render Free Shutdown បិទ Bot
flask_app = Flask('')

@flask_app.route('/')
def home():
    return "Bot is alive!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    flask_app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = threading.Thread(target=run_flask)
    t.daemon = True
    t.start()

# ហៅ Web Server ឱ្យដំណើរការជា Background
keep_alive()

# ២. កំណត់យក Token ពី Render Environment 
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("សួស្តី 👋 ខ្ញុំជា AI Bot។ សួរខ្ញុំបាន!")

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": update.message.text}]
        )
        output_text = response.choices.message.content
        await update.message.reply_text(output_text)
    except Exception as e:
        print(f"Error: {e}")
        await update.message.reply_text("សូមអភ័យទោស មានបញ្ហាបច្ចេកទេសបន្តិចបន្តួច។")

def main():
    # ៣. Setup Telegram Bot Application
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    
    # រត់ Bot ទាញទិន្នន័យ
    app.run_polling()

if __name__ == '__main__':
    main()

