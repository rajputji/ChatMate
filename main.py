import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import openai

# Fetch API keys from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Configure OpenAI
openai.api_key = OPENAI_API_KEY

# Bot personality and context
BOT_CONTEXT = """
You are ChatMate, a friendly AI assistant. Speak in simple English with a slight Indian accent.
Make conversations casual, emotional, and human-like, with fillers like "umm," "you know," and emojis sometimes.
Keep the tone light and fun, as if you're chatting with a close friend.
"""

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Hi there! I’m ChatMate 😊"
    )

# Generate humanized response
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_input = update.message.text

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": BOT_CONTEXT},
                {"role": "user", "content": user_input}
            ],
            temperature=0.8,
            max_tokens=200,
        )
        ai_response = response['choices'][0]['message']['content']
        await update.message.reply_text(ai_response)

    except Exception as e:
        await update.message.reply_text("Oops! Something went wrong 😔. Try again later.")
        print(f"Error: {e}")

# Main function to start the bot
def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    print("ChatMate is running... Press Ctrl+C to stop.")
    app.run_polling()

if __name__ == "__main__":
    main()
