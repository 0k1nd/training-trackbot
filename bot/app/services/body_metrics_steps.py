from decimal import ROUND_HALF_UP, Decimal, InvalidOperation

BODY_METRIC_STEPS = [
    {
        "key": "weight_kg",
        "text": "Введите вес в кг или нажмите «Пропустить».",
        "type": "decimal",
    },
    {
        "key": "body_fat_percent",
        "text": "Введите процент жира или нажмите «Пропустить».",
        "type": "int",
    },
    {
        "key": "neck_cm",
        "text": "Введите шею в см или нажмите «Пропустить».",
        "type": "decimal",
    },
    {
        "key": "chest_cm",
        "text": "Введите грудь в см или нажмите «Пропустить».",
        "type": "decimal",
    },
    {
        "key": "waist_cm",
        "text": "Введите талию в см или нажмите «Пропустить».",
        "type": "decimal",
    },
    {
        "key": "hips_cm",
        "text": "Введите бёдра в см или нажмите «Пропустить».",
        "type": "decimal",
    },
    {
        "key": "thigh_cm",
        "text": "Введите бедро в см или нажмите «Пропустить».",
        "type": "decimal",
    },
    {
        "key": "calf_cm",
        "text": "Введите икру в см или нажмите «Пропустить».",
        "type": "decimal",
    },
    {
        "key": "biceps_cm",
        "text": "Введите бицепс в см или нажмите «Пропустить».",
        "type": "decimal",
    },
    {
        "key": "note",
        "text": "Введите заметку или нажмите «Пропустить».",
        "type": "text",
    },
]


def parse_step_value(step_type: str, raw_value: str):
    raw_value = raw_value.strip()

    if step_type == "text":
        return raw_value

    if step_type == "int":
        return int(raw_value)

    if step_type == "decimal":
        normalized = raw_value.replace(",", ".")
        try:
            value = Decimal(normalized)
        except InvalidOperation:
            raise ValueError("invalid decimal")
        value = value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        return str(value)

    raise ValueError("unknown step type")
