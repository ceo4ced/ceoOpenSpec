import os
import logging
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Takes the role of the CEO Agent introducing itself."""
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="👋 Hello Founder. I am your AI CEO. I am ready to receive your business vision. What should we build today?"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Forwards messages to the CEO Agent Cloud Function.
    In a real deployment, this would make an HTTP request to the GCP Cloud Function.
    """
    user_text = update.message.text
    user_id = update.effective_user.id
    
    logging.info(f"Received from {user_id}: {user_text}")
    
    # Mock response from CEO Agent
    # TODO: Connect to functions/ceo via HTTP
    response_text = f"I have received your instruction: '{user_text}'. I am thinking about the strategic implications..."
    
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=response_text
    )

if __name__ == '__main__':
    # Load token from environment variable
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        print("Error: TELEGRAM_BOT_TOKEN environment variable not set.")
        exit(1)
        
    application = ApplicationBuilder().token(token).build()
    
    start_handler = CommandHandler('start', start)
    message_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message)
    
    application.add_handler(start_handler)
    application.add_handler(message_handler)
    
    print("CEO Agent Telegram Bot is running...")
    application.run_polling()
