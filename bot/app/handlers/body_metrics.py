from decimal import ROUND_HALF_UP, Decimal, InvalidOperation

from telegram import Update
from telegram.ext import (
    CallbackQueryHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from app.conversations.states import BodyMetricStates
from app.keyboards.body_metrics import body_metrics_menu_keyboard
from app.services.body_metrics_pagination import (
    render_body_metrics_page,
    render_body_metrics_page_after_delete,
)


def _parse_optional_decimal(value: str) -> str | None:
    value = value.strip()
    if value == "-":
        return None

    normalized = value.replace(",", ".")

    try:
        decimal_value = Decimal(normalized)
    except InvalidOperation:
        raise ValueError("invalid decimal")

    decimal_value = decimal_value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return str(decimal_value)


def _parse_optional_int(value: str) -> int | None:
    value = value.strip()
    if value == "-":
        return None
    return int(value)


async def body_metrics_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    await query.edit_message_text(
        text="Параметры тела",
        reply_markup=body_metrics_menu_keyboard(),
    )


async def body_metrics_list_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    parts = query.data.split(":")
    offset = int(parts[2]) if len(parts) > 2 else 0

    await render_body_metrics_page(query, context, offset)


async def body_metric_add_start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    context.user_data["body_metric_payload"] = {}

    await query.edit_message_text("Введите вес в кг или отправьте '-'")
    return BodyMetricStates.WAITING_WEIGHT


async def body_metric_weight_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        value = _parse_optional_decimal(update.message.text)
    except ValueError:
        await update.message.reply_text("Введите число или '-'")
        return BodyMetricStates.WAITING_WEIGHT

    if value is not None:
        context.user_data["body_metric_payload"]["weight_kg"] = value

    await update.message.reply_text("Введите процент жира или отправьте '-'")
    return BodyMetricStates.WAITING_BODY_FAT_PERCENT


async def body_metric_body_fat_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        value = _parse_optional_int(update.message.text)
    except ValueError:
        await update.message.reply_text("Введите целое число или '-'")
        return BodyMetricStates.WAITING_BODY_FAT_PERCENT

    if value is not None:
        context.user_data["body_metric_payload"]["body_fat_percent"] = value

    await update.message.reply_text("Введите шею в см или отправьте '-'")
    return BodyMetricStates.WAITING_NECK


async def body_metric_neck_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        value = _parse_optional_decimal(update.message.text)
    except ValueError:
        await update.message.reply_text("Введите число или '-'")
        return BodyMetricStates.WAITING_NECK

    if value is not None:
        context.user_data["body_metric_payload"]["neck_cm"] = value

    await update.message.reply_text("Введите грудь в см или отправьте '-'")
    return BodyMetricStates.WAITING_CHEST


async def body_metric_chest_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        value = _parse_optional_decimal(update.message.text)
    except ValueError:
        await update.message.reply_text("Введите число или '-'")
        return BodyMetricStates.WAITING_CHEST

    if value is not None:
        context.user_data["body_metric_payload"]["chest_cm"] = value

    await update.message.reply_text("Введите талию в см или отправьте '-'")
    return BodyMetricStates.WAITING_WAIST


async def body_metric_waist_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        value = _parse_optional_decimal(update.message.text)
    except ValueError:
        await update.message.reply_text("Введите число или '-'")
        return BodyMetricStates.WAITING_WAIST

    if value is not None:
        context.user_data["body_metric_payload"]["waist_cm"] = value

    await update.message.reply_text("Введите бёдра в см или отправьте '-'")
    return BodyMetricStates.WAITING_HIPS


async def body_metric_hips_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        value = _parse_optional_decimal(update.message.text)
    except ValueError:
        await update.message.reply_text("Введите число или '-'")
        return BodyMetricStates.WAITING_HIPS

    if value is not None:
        context.user_data["body_metric_payload"]["hips_cm"] = value

    await update.message.reply_text("Введите бедро в см или отправьте '-'")
    return BodyMetricStates.WAITING_THIGH


async def body_metric_thigh_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        value = _parse_optional_decimal(update.message.text)
    except ValueError:
        await update.message.reply_text("Введите число или '-'")
        return BodyMetricStates.WAITING_THIGH

    if value is not None:
        context.user_data["body_metric_payload"]["thigh_cm"] = value

    await update.message.reply_text("Введите икру в см или отправьте '-'")
    return BodyMetricStates.WAITING_CALF


async def body_metric_calf_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        value = _parse_optional_decimal(update.message.text)
    except ValueError:
        await update.message.reply_text("Введите число или '-'")
        return BodyMetricStates.WAITING_CALF

    if value is not None:
        context.user_data["body_metric_payload"]["calf_cm"] = value

    await update.message.reply_text("Введите бицепс в см или отправьте '-'")
    return BodyMetricStates.WAITING_BICEPS


async def body_metric_biceps_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        value = _parse_optional_decimal(update.message.text)
    except ValueError:
        await update.message.reply_text("Введите число или '-'")
        return BodyMetricStates.WAITING_BICEPS

    if value is not None:
        context.user_data["body_metric_payload"]["biceps_cm"] = value

    await update.message.reply_text("Введите заметку или отправьте '-'")
    return BodyMetricStates.WAITING_NOTE


async def body_metric_note_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    value = update.message.text.strip()

    if value != "-":
        context.user_data["body_metric_payload"]["note"] = value

    api_client = context.application.bot_data["api_client"]
    payload = context.user_data.get("body_metric_payload", {})

    await api_client.create_body_metric(
        chat_id=update.effective_user.id,
        payload=payload,
    )

    context.user_data.pop("body_metric_payload", None)

    await update.message.reply_text(
        text="Параметры тела сохранены.",
        reply_markup=body_metrics_menu_keyboard(),
    )
    return ConversationHandler.END


async def body_metric_delete_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    parts = query.data.split(":")
    metric_id = int(parts[2])
    offset = int(parts[3]) if len(parts) > 3 else 0

    api_client = context.application.bot_data["api_client"]

    await api_client.delete_body_metric(
        chat_id=query.from_user.id,
        metric_id=metric_id,
    )

    await render_body_metrics_page_after_delete(query, context, offset)


def build_body_metrics_conversation():
    return ConversationHandler(
        entry_points=[
            CallbackQueryHandler(body_metric_add_start_handler, pattern=r"^body:add$"),
        ],
        states={
            BodyMetricStates.WAITING_WEIGHT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, body_metric_weight_handler),
            ],
            BodyMetricStates.WAITING_BODY_FAT_PERCENT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, body_metric_body_fat_handler),
            ],
            BodyMetricStates.WAITING_NECK: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, body_metric_neck_handler),
            ],
            BodyMetricStates.WAITING_CHEST: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, body_metric_chest_handler),
            ],
            BodyMetricStates.WAITING_WAIST: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, body_metric_waist_handler),
            ],
            BodyMetricStates.WAITING_HIPS: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, body_metric_hips_handler),
            ],
            BodyMetricStates.WAITING_THIGH: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, body_metric_thigh_handler),
            ],
            BodyMetricStates.WAITING_CALF: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, body_metric_calf_handler),
            ],
            BodyMetricStates.WAITING_BICEPS: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, body_metric_biceps_handler),
            ],
            BodyMetricStates.WAITING_NOTE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, body_metric_note_handler),
            ],
        },
        fallbacks=[],
        per_chat=True,
        per_user=True,
    )


def register_body_metrics_handlers(application):
    application.add_handler(CallbackQueryHandler(body_metrics_menu_handler, pattern=r"^body:menu$"))
    application.add_handler(
        CallbackQueryHandler(body_metrics_list_handler, pattern=r"^body:list(?::\d+)?$")
    )
    application.add_handler(
        CallbackQueryHandler(body_metric_delete_handler, pattern=r"^body:delete:\d+:\d+$")
    )
    application.add_handler(build_body_metrics_conversation())
