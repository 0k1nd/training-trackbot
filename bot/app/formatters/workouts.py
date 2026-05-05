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
