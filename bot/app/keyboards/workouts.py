from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def workout_menu_keyboard(has_active_workout: bool) -> InlineKeyboardMarkup:
    rows = []

    if has_active_workout:
        rows.append(
            [InlineKeyboardButton("Продолжить тренировку", callback_data="workout:continue")]
        )
        rows.append([InlineKeyboardButton("Завершить тренировку", callback_data="workout:finish")])
    else:
        rows.append([InlineKeyboardButton("Начать тренировку", callback_data="workout:start")])

    rows.append([InlineKeyboardButton("Назад", callback_data="menu:main")])

    return InlineKeyboardMarkup(rows)


def active_workout_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Выбрать упражнение", callback_data="exercise:list")],
            [InlineKeyboardButton("Завершить тренировку", callback_data="workout:finish")],
            [InlineKeyboardButton("Назад", callback_data="workout:menu")],
        ]
    )
