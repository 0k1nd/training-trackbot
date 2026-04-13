from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

from app.keyboards.common import start_keyboard


async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tg_user = update.effective_user
    api_client = context.application.bot_data["api_client"]

    await api_client.register_user(
        chat_id=tg_user.id,
        username=tg_user.username,
        first_name=tg_user.first_name,
        last_name=tg_user.last_name,
    )

    await update.message.reply_text(
        text="Привет. Это бот для тренировок и отслеживания прогресса.",
        reply_markup=start_keyboard(),
    )


def register_start_handlers(application):
    application.add_handler(CommandHandler("start", start_handler))
