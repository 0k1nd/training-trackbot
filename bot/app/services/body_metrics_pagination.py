from telegram import CallbackQuery
from telegram.ext import ContextTypes

from app.formatters.body_metrics import format_body_metrics_page
from app.keyboards.body_metrics import body_metrics_list_keyboard

BODY_METRICS_PAGE_LIMIT = 5


async def render_body_metrics_page(
    query: CallbackQuery,
    context: ContextTypes.DEFAULT_TYPE,
    offset: int = 0,
):
    api_client = context.application.bot_data["api_client"]

    data = await api_client.list_body_metrics(
        chat_id=query.from_user.id,
        limit=BODY_METRICS_PAGE_LIMIT,
        offset=offset,
    )

    await query.edit_message_text(
        text=format_body_metrics_page(data),
        reply_markup=body_metrics_list_keyboard(
            metrics=data["results"],
            offset=data["offset"],
            next_offset=data["next_offset"],
            prev_offset=data["prev_offset"],
        ),
    )


async def render_body_metrics_page_after_delete(
    query: CallbackQuery,
    context: ContextTypes.DEFAULT_TYPE,
    offset: int = 0,
):
    api_client = context.application.bot_data["api_client"]

    data = await api_client.list_body_metrics(
        chat_id=query.from_user.id,
        limit=BODY_METRICS_PAGE_LIMIT,
        offset=offset,
    )

    if not data["results"] and offset > 0:
        new_offset = max(0, offset - data["limit"])
        data = await api_client.list_body_metrics(
            chat_id=query.from_user.id,
            limit=BODY_METRICS_PAGE_LIMIT,
            offset=new_offset,
        )

    await query.edit_message_text(
        text="Запись удалена.\n\n" + format_body_metrics_page(data),
        reply_markup=body_metrics_list_keyboard(
            metrics=data["results"],
            offset=data["offset"],
            next_offset=data["next_offset"],
            prev_offset=data["prev_offset"],
        ),
    )
