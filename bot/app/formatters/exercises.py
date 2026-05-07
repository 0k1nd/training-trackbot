def format_exercise_detail(data: dict) -> str:
    lines = [
        f"{data['name']}",
        "",
        f"Основная группа: {data.get('primary_muscle') or '-'}",
        f"Доп. группа: {data.get('secondary_muscle') or '-'}",
        f"Оборудование: {data.get('equipment') or '-'}",
        f"Тип: {'базовое' if data.get('is_basic') else 'своё'}",
    ]

    if data.get("description"):
        lines.extend(["", data["description"]])

    return "\n".join(lines)
