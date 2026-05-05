from telegram import Update
from telegram.ext import CallbackQueryHandler, ContextTypes

from app.api.exceptions import BackendApiError, BackendValidationError
from app.formatters.workouts import format_workouts
from app.keyboards.workouts import (
    active_workout_keyboard,
    workout_history_keyboard,
    workout_menu_keyboard,
)


async def workout_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    api_client = context.application.bot_data["api_client"]

    try:
        workout = await api_client.get_current_workout(chat_id=query.from_user.id)
        context.user_data["workout_id"] = workout["id"]
        has_active = True
    except BackendApiError:
        has_active = False

    await query.edit_message_text(
        text="Раздел тренировок",
        reply_markup=workout_menu_keyboard(has_active),
    )


async def workout_list_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    api_client = context.application.bot_data["api_client"]
    workouts = await api_client.list_workouts(chat_id=query.from_user.id)

    await query.edit_message_text(
        text=format_workouts(workouts),
        reply_markup=workout_history_keyboard(),
    )


async def start_workout_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    api_client = context.application.bot_data["api_client"]

    try:
        workout = await api_client.start_workout(chat_id=query.from_user.id)
    except BackendValidationError:
        workout = await api_client.get_current_workout(chat_id=query.from_user.id)

    workout_id = workout.get("workout_id") or workout.get("id")
    context.user_data["workout_id"] = workout_id

    await query.edit_message_text(
        text="Тренировка начата. Выберите упражнение.",
        reply_markup=active_workout_keyboard(),
    )


async def continue_workout_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    api_client = context.application.bot_data["api_client"]

    try:
        workout = await api_client.get_current_workout(chat_id=query.from_user.id)
    except BackendApiError:
        await query.edit_message_text(
            text="Активной тренировки нет.",
            reply_markup=workout_menu_keyboard(False),
        )
        return

    context.user_data["workout_id"] = workout["id"]

    await query.edit_message_text(
        text=f"Активная тренировка #{workout['id']}",
        reply_markup=active_workout_keyboard(),
    )


async def finish_workout_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    workout_id = context.user_data.get("workout_id")
    api_client = context.application.bot_data["api_client"]

    if not workout_id:
        try:
            workout = await api_client.get_current_workout(chat_id=query.from_user.id)
            workout_id = workout["id"]
        except BackendApiError:
            await query.edit_message_text("Активной тренировки нет.")
            return

    await api_client.finish_workout(
        chat_id=query.from_user.id,
        workout_id=workout_id,
    )

    context.user_data.pop("workout_id", None)
    context.user_data.pop("workout_exercise_id", None)
    context.user_data.pop("exercise_name", None)
    context.user_data.pop("pending_set", None)

    await query.edit_message_text(
        text="Тренировка завершена.",
        reply_markup=workout_menu_keyboard(False),
    )


def register_workout_handlers(application):
    application.add_handler(CallbackQueryHandler(workout_menu_handler, pattern=r"^workout:menu$"))
    application.add_handler(CallbackQueryHandler(workout_list_handler, pattern=r"^workout:list$"))
    application.add_handler(CallbackQueryHandler(start_workout_handler, pattern=r"^workout:start$"))
    application.add_handler(
        CallbackQueryHandler(continue_workout_handler, pattern=r"^workout:continue$")
    )
    application.add_handler(
        CallbackQueryHandler(finish_workout_handler, pattern=r"^workout:finish$")
    )
