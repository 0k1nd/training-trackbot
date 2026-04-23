from telegram import Update
from telegram.ext import (
    CallbackQueryHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from app.conversations.states import BodyMetricStates
from app.keyboards.body_metrics import (
    body_metrics_menu_keyboard,
    body_metrics_step_keyboard,
)
from app.services.body_metrics_pagination import render_body_metrics_page
from app.services.body_metrics_steps import BODY_METRIC_STEPS, parse_step_value


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


async def _show_current_step(target, context: ContextTypes.DEFAULT_TYPE):
    step_index = context.user_data.get("body_metric_step", 0)
    step = BODY_METRIC_STEPS[step_index]

    text = f"Шаг {step_index + 1} из {len(BODY_METRIC_STEPS)}\n\n{step['text']}"

    if hasattr(target, "edit_message_text"):
        await target.edit_message_text(
            text=text,
            reply_markup=body_metrics_step_keyboard(),
        )
    else:
        await target.reply_text(
            text=text,
            reply_markup=body_metrics_step_keyboard(),
        )


async def body_metric_add_start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    context.user_data["body_metric_payload"] = {}
    context.user_data["body_metric_step"] = 0

    await _show_current_step(query, context)
    return BodyMetricStates.WAITING_VALUE


async def body_metric_value_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    step_index = context.user_data.get("body_metric_step", 0)
    step = BODY_METRIC_STEPS[step_index]
    payload = context.user_data.setdefault("body_metric_payload", {})

    raw_value = update.message.text.strip()

    try:
        value = parse_step_value(step["type"], raw_value)
    except ValueError:
        await update.message.reply_text(
            "Неверный формат. Попробуйте ещё раз.",
            reply_markup=body_metrics_step_keyboard(),
        )
        return BodyMetricStates.WAITING_VALUE

    payload[step["key"]] = value

    next_step = step_index + 1
    context.user_data["body_metric_step"] = next_step

    if next_step >= len(BODY_METRIC_STEPS):
        api_client = context.application.bot_data["api_client"]

        await api_client.create_body_metric(
            chat_id=update.effective_user.id,
            payload=payload,
        )

        context.user_data.pop("body_metric_payload", None)
        context.user_data.pop("body_metric_step", None)

        await update.message.reply_text(
            text="Параметры тела сохранены.",
            reply_markup=body_metrics_menu_keyboard(),
        )
        return ConversationHandler.END

    await _show_current_step(update.message, context)
    return BodyMetricStates.WAITING_VALUE


async def body_metric_step_back_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    step_index = context.user_data.get("body_metric_step", 0)
    payload = context.user_data.setdefault("body_metric_payload", {})

    if step_index > 0:
        current_step_key = (
            BODY_METRIC_STEPS[step_index]["key"] if step_index < len(BODY_METRIC_STEPS) else None
        )
        if current_step_key:
            payload.pop(current_step_key, None)

        context.user_data["body_metric_step"] = step_index - 1

    await _show_current_step(query, context)
    return BodyMetricStates.WAITING_VALUE


async def body_metric_step_skip_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    step_index = context.user_data.get("body_metric_step", 0)
    payload = context.user_data.setdefault("body_metric_payload", {})

    step = BODY_METRIC_STEPS[step_index]
    payload.pop(step["key"], None)

    next_step = step_index + 1
    context.user_data["body_metric_step"] = next_step

    if next_step >= len(BODY_METRIC_STEPS):
        api_client = context.application.bot_data["api_client"]

        await api_client.create_body_metric(
            chat_id=query.from_user.id,
            payload=payload,
        )

        context.user_data.pop("body_metric_payload", None)
        context.user_data.pop("body_metric_step", None)

        await query.edit_message_text(
            text="Параметры тела сохранены.",
            reply_markup=body_metrics_menu_keyboard(),
        )
        return ConversationHandler.END

    await _show_current_step(query, context)
    return BodyMetricStates.WAITING_VALUE


async def body_metric_step_cancel_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    context.user_data.pop("body_metric_payload", None)
    context.user_data.pop("body_metric_step", None)

    await query.edit_message_text(
        text="Добавление параметров отменено.",
        reply_markup=body_metrics_menu_keyboard(),
    )
    return ConversationHandler.END


def build_body_metrics_conversation():
    return ConversationHandler(
        entry_points=[
            CallbackQueryHandler(body_metric_add_start_handler, pattern=r"^body:add$"),
        ],
        states={
            BodyMetricStates.WAITING_VALUE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, body_metric_value_handler),
                CallbackQueryHandler(body_metric_step_back_handler, pattern=r"^body:step:back$"),
                CallbackQueryHandler(body_metric_step_skip_handler, pattern=r"^body:step:skip$"),
                CallbackQueryHandler(
                    body_metric_step_cancel_handler, pattern=r"^body:step:cancel$"
                ),
            ],
        },
        fallbacks=[
            CallbackQueryHandler(body_metric_step_cancel_handler, pattern=r"^body:step:cancel$"),
        ],
        per_chat=True,
        per_user=True,
    )


def register_body_metrics_handlers(application):
    application.add_handler(CallbackQueryHandler(body_metrics_menu_handler, pattern=r"^body:menu$"))
    application.add_handler(
        CallbackQueryHandler(body_metrics_list_handler, pattern=r"^body:list(?::\d+)?$")
    )
    application.add_handler(build_body_metrics_conversation())
