from telegram import Update
from telegram.ext import CallbackQueryHandler, ContextTypes

from app.keyboards.common import main_menu_keyboard


async def main_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    await query.edit_message_text(
        text="Главное меню",
        reply_markup=main_menu_keyboard(),
    )


def register_menu_handlers(application):
    application.add_handler(CallbackQueryHandler(main_menu_handler, pattern=r"^menu:main$"))
