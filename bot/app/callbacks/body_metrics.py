from app.callbacks.prefixes import BODY


def body_menu() -> str:
    return f"{BODY}:menu"


def body_add() -> str:
    return f"{BODY}:add"


def body_list() -> str:
    return f"{BODY}:list"


def body_delete(metric_id: int) -> str:
    return f"{BODY}:delete:{metric_id}"


def body_back() -> str:
    return f"{BODY}:back"
