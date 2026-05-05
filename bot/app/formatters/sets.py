DIFFICULTY_LABELS = {
    "easy": "легко",
    "moderate": "средне",
    "hard": "тяжело",
}


def format_workout_exercise_sets(data: dict) -> str:
    exercise_name = data["exercise"]["name"]
    sets = data.get("sets", [])

    lines = [f"{exercise_name}\n"]

    if not sets:
        lines.append("Подходов пока нет.")
        return "\n".join(lines)

    for item in sets:
        weight = item.get("weight")
        reps = item.get("reps")
        difficulty = DIFFICULTY_LABELS.get(item.get("difficulty"), item.get("difficulty"))

        if weight is not None and reps is not None:
            lines.append(f"{item['set_number']}. {weight} × {reps}, {difficulty}")
        elif reps is not None:
            lines.append(f"{item['set_number']}. {reps} повторений, {difficulty}")
        else:
            lines.append(f"{item['set_number']}. {weight} кг, {difficulty}")

    return "\n".join(lines)
