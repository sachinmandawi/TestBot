"""Minimal async Telegram echo bot (python-telegram-bot v20).

Usage:
  1. copy `.env.example` -> `.env` and set TELEGRAM_TOKEN
  2. pip install -r requirements.txt
  3. python bot.py
"""
import os
# from dotenv import load_dotenv  # Not needed for hardcoded
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# load_dotenv()
TOKEN = "8439636405:AAGXgC3kX5gf2o_bVcbKPrUb2NIApvFtLi0"  # Replace with your actual token

def create_application(token: str | None = None):
    """Return an Application instance. Raises RuntimeError if token is missing."""
    token = token or os.getenv("TELEGRAM_TOKEN") or TOKEN
    if not token:
        raise RuntimeError(
            "Missing TELEGRAM_TOKEN. Provide a token to create_application(token) "
            "or set the TELEGRAM_TOKEN environment variable (see .env.example)."
        )

    app = ApplicationBuilder().token(token).build()
    # handlers are attached here so tests can import handler callables without starting the bot
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    return app

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = (update.effective_user.first_name if update.effective_user else "there")
    await update.message.reply_text(
        f"Hello {user}! This is a testing bot — send me any message and I'll echo it back."
    )

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(update.message.text)

def main() -> None:
    try:
        app = create_application(TOKEN)
    except RuntimeError as exc:
        raise SystemExit(str(exc))

    print("Bot started (polling). Press Ctrl-C to stop.")
    app.run_polling()


if __name__ == "__main__":
    main()


