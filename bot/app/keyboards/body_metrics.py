from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def body_metrics_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(text="Добавить запись", callback_data="body:add")],
            [InlineKeyboardButton(text="Мои записи", callback_data="body:list:0")],
            [InlineKeyboardButton(text="Назад", callback_data="menu:main")],
        ]
    )


def body_metrics_list_keyboard(
    metrics: list[dict],
    offset: int,
    next_offset: int | None,
    prev_offset: int | None,
) -> InlineKeyboardMarkup:
    rows = []

    for item in metrics:
        rows.append(
            [
                InlineKeyboardButton(
                    text=f"Удалить #{item['id']}",
                    callback_data=f"body:delete:{item['id']}:{offset}",
                )
            ]
        )

    nav_row = []

    if prev_offset is not None:
        nav_row.append(
            InlineKeyboardButton(
                text="⬅️ Назад",
                callback_data=f"body:list:{prev_offset}",
            )
        )

    if next_offset is not None:
        nav_row.append(
            InlineKeyboardButton(
                text="Вперёд ➡️",
                callback_data=f"body:list:{next_offset}",
            )
        )

    if nav_row:
        rows.append(nav_row)

    rows.append([InlineKeyboardButton(text="Назад", callback_data="body:menu")])

    return InlineKeyboardMarkup(rows)
