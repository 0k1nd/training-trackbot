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

    rows.append([InlineKeyboardButton("История тренировок", callback_data="workout:list")])
    rows.append([InlineKeyboardButton("Назад", callback_data="menu:main")])

    return InlineKeyboardMarkup(rows)


def workout_history_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Назад к тренировкам", callback_data="workout:menu")],
            [InlineKeyboardButton("Главное меню", callback_data="menu:main")],
        ]
    )


def active_workout_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Каталог упражнений", callback_data="exercise:catalog")],
            [InlineKeyboardButton("Поиск упражнения", callback_data="exercise:search")],
            [InlineKeyboardButton("Создать своё упражнение", callback_data="exercise:create")],
            [InlineKeyboardButton("Завершить тренировку", callback_data="workout:finish")],
            [InlineKeyboardButton("Назад", callback_data="workout:menu")],
        ]
    )
