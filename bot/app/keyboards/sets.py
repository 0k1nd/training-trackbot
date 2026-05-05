from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def set_difficulty_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Легко", callback_data="set:difficulty:easy"),
                InlineKeyboardButton("Средне", callback_data="set:difficulty:moderate"),
                InlineKeyboardButton("Тяжело", callback_data="set:difficulty:hard"),
            ],
            [InlineKeyboardButton("Отмена", callback_data="workout:continue")],
        ]
    )
