from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def exercise_catalog_keyboard(groups: list[dict]) -> InlineKeyboardMarkup:
    rows = []

    for group in groups:
        rows.append(
            [
                InlineKeyboardButton(
                    text=group["muscle"],
                    callback_data=f"exercise:group:{group['muscle']}",
                )
            ]
        )

    rows.append([InlineKeyboardButton("Поиск", callback_data="exercise:search")])
    rows.append([InlineKeyboardButton("Создать своё", callback_data="exercise:create")])
    rows.append([InlineKeyboardButton("Назад", callback_data="workout:continue")])

    return InlineKeyboardMarkup(rows)


def exercise_group_keyboard(group: dict) -> InlineKeyboardMarkup:
    rows = []

    for item in group["items"][:20]:
        rows.append(
            [
                InlineKeyboardButton(
                    text=item["name"],
                    callback_data=f"exercise:pick:{item['id']}:{item['equipment']}",
                )
            ]
        )

    rows.append([InlineKeyboardButton("Назад к группам", callback_data="exercise:catalog")])

    return InlineKeyboardMarkup(rows)


def exercises_keyboard(exercises: list[dict]) -> InlineKeyboardMarkup:
    rows = []

    for item in exercises[:20]:
        rows.append(
            [
                InlineKeyboardButton(
                    text=item["name"],
                    callback_data=f"exercise:pick:{item['id']}:{item['equipment']}",
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
