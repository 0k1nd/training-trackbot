from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def exercises_keyboard(exercises: list[dict]) -> InlineKeyboardMarkup:
    rows = []

    for item in exercises[:20]:
        rows.append(
            [
                InlineKeyboardButton(
                    text=item["name"],
                    callback_data=f"exercise:pick:{item['id']}",
                )
            ]
        )

    rows.append([InlineKeyboardButton("Назад", callback_data="workout:continue")])

    return InlineKeyboardMarkup(rows)


def workout_exercise_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Добавить подход", callback_data="set:add")],
            [InlineKeyboardButton("Повторить последний", callback_data="set:repeat")],
            [InlineKeyboardButton("Завершить упражнение", callback_data="exercise:finish")],
            [InlineKeyboardButton("Завершить тренировку", callback_data="workout:finish")],
        ]
    )
