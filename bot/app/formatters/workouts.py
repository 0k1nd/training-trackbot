def format_workouts(workouts: list[dict]) -> str:
    if not workouts:
        return "Тренировок пока нет."

    lines = ["Последние тренировки:\n"]

    for item in workouts:
        status = "завершена" if item.get("finished_at") else "активная"
        lines.append(
            f"#{item['id']} — {status}, "
            f"упражнений: {item['exercises_count']}, "
            f"подходов: {item['sets_count']}"
        )

    return "\n".join(lines)


def format_workout_detail(data: dict) -> str:
    status = "завершена" if data.get("finished_at") else "активная"
    lines = [
        f"Тренировка #{data['id']}",
        f"Статус: {status}",
        "",
    ]

    items = data.get("items", [])
    if not items:
        lines.append("Упражнений пока нет.")
        return "\n".join(lines)

    for item in items:
        lines.append(f"{item['order']}. {item['exercise']['name']}")

        sets = item.get("sets", [])
        if not sets:
            lines.append("   подходов нет")
            continue

        for set_obj in sets:
            weight = set_obj.get("weight")
            reps = set_obj.get("reps")

            if weight is not None and reps is not None:
                lines.append(f"   {set_obj['set_number']}) {weight} × {reps}")
            elif reps is not None:
                lines.append(f"   {set_obj['set_number']}) {reps} повторений")
            elif weight is not None:
                lines.append(f"   {set_obj['set_number']}) {weight} кг")

    return "\n".join(lines)
