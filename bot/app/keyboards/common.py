from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def start_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(text="Начать", callback_data="menu:main")],
        ]
    )


def main_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(text="Тренировки", callback_data="workout:menu")],
            [InlineKeyboardButton(text="Параметры тела", callback_data="body:menu")],
        ]
    )
