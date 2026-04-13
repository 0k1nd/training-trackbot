def format_body_metrics_page(data: dict) -> str:
    metrics = data.get("results", [])
    count = data.get("count", 0)
    limit = data.get("limit", 5)
    offset = data.get("offset", 0)

    if not metrics:
        return "У вас пока нет сохранённых параметров тела."

    page_number = offset // limit + 1 if limit else 1
    total_pages = ((count - 1) // limit + 1) if count else 1

    lines = [f"Параметры тела\nСтраница {page_number} из {total_pages}\n"]

    for item in metrics:
        parts = [f"#{item['id']}"]

        if item.get("weight_kg") is not None:
            parts.append(f"вес: {item['weight_kg']} кг")
        if item.get("body_fat_percent") is not None:
            parts.append(f"жир: {item['body_fat_percent']}%")
        if item.get("neck_cm") is not None:
            parts.append(f"шея: {item['neck_cm']} см")
        if item.get("chest_cm") is not None:
            parts.append(f"грудь: {item['chest_cm']} см")
        if item.get("waist_cm") is not None:
            parts.append(f"талия: {item['waist_cm']} см")
        if item.get("hips_cm") is not None:
            parts.append(f"бёдра: {item['hips_cm']} см")
        if item.get("thigh_cm") is not None:
            parts.append(f"бедро: {item['thigh_cm']} см")
        if item.get("calf_cm") is not None:
            parts.append(f"икра: {item['calf_cm']} см")
        if item.get("biceps_cm") is not None:
            parts.append(f"бицепс: {item['biceps_cm']} см")
        if item.get("note"):
            parts.append(f"заметка: {item['note']}")

        lines.append("• " + ", ".join(parts))

    return "\n".join(lines)
