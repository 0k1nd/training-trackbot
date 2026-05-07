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
                    callback_data=f"exercise:detail:{item['id']}",
                )
            ]
        )

    rows.append([InlineKeyboardButton("Назад", callback_data="workout:continue")])
    return InlineKeyboardMarkup(rows)


def exercise_detail_keyboard(exercise_id: int, equipment: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "Добавить в тренировку",
                    callback_data=f"exercise:pick:{exercise_id}:{equipment}",
                )
            ],
            [InlineKeyboardButton("Назад к каталогу", callback_data="exercise:catalog")],
        ]
    )


def muscle_select_keyboard() -> InlineKeyboardMarkup:
    muscles = [
        ("Грудь", "chest"),
        ("Спина", "back"),
        ("Ноги", "legs"),
        ("Плечи", "shoulders"),
        ("Бицепс", "biceps"),
        ("Трицепс", "triceps"),
        ("Пресс", "abs"),
    ]

    rows = [
        [InlineKeyboardButton(label, callback_data=f"exercise:create:muscle:{value}")]
        for label, value in muscles
    ]
    rows.append([InlineKeyboardButton("Отмена", callback_data="workout:continue")])
    return InlineKeyboardMarkup(rows)


def equipment_select_keyboard() -> InlineKeyboardMarkup:
    equipment = [
        ("Собственный вес", "bodyweight"),
        ("Штанга", "barbell"),
        ("Гантели", "dumbbell"),
        ("Тренажёр", "machine"),
        ("Другое", "other"),
    ]

    rows = [
        [InlineKeyboardButton(label, callback_data=f"exercise:create:equipment:{value}")]
        for label, value in equipment
    ]
    rows.append([InlineKeyboardButton("Отмена", callback_data="workout:continue")])
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
