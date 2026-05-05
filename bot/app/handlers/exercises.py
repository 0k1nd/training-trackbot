from telegram import Update
from telegram.ext import CallbackQueryHandler, ContextTypes

from app.keyboards.exercises import (
    exercise_catalog_keyboard,
    exercise_group_keyboard,
    workout_exercise_keyboard,
)
from app.keyboards.workouts import active_workout_keyboard


async def exercise_catalog_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    api_client = context.application.bot_data["api_client"]
    groups = await api_client.get_exercise_catalog(chat_id=query.from_user.id)

    context.user_data["exercise_catalog"] = groups

    await query.edit_message_text(
        text="Выберите группу мышц:",
        reply_markup=exercise_catalog_keyboard(groups),
    )


async def exercise_group_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    muscle = query.data.split(":")[2]
    groups = context.user_data.get("exercise_catalog", [])

    group = next((item for item in groups if item["muscle"] == muscle), None)

    if not group:
        await query.edit_message_text("Группа не найдена.")
        return

    await query.edit_message_text(
        text=f"Упражнения: {muscle}",
        reply_markup=exercise_group_keyboard(group),
    )


async def exercise_pick_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    parts = query.data.split(":")
    exercise_id = int(parts[2])
    equipment = parts[3]

    context.user_data["exercise_equipment"] = equipment

    workout_id = context.user_data.get("workout_id")
    api_client = context.application.bot_data["api_client"]

    if not workout_id:
        workout = await api_client.get_current_workout(chat_id=query.from_user.id)
        workout_id = workout["id"]
        context.user_data["workout_id"] = workout_id

    item = await api_client.add_exercise_to_workout(
        chat_id=query.from_user.id,
        workout_id=workout_id,
        exercise_id=exercise_id,
    )

    context.user_data["workout_exercise_id"] = item["workout_exercise_id"]
    context.user_data["exercise_name"] = item["exercise_name"]

    await query.edit_message_text(
        text=f"Упражнение: {item['exercise_name']}\nДобавьте первый подход.",
        reply_markup=workout_exercise_keyboard(),
    )


async def exercise_finish_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    workout_exercise_id = context.user_data.get("workout_exercise_id")
    api_client = context.application.bot_data["api_client"]

    if not workout_exercise_id:
        await query.edit_message_text(
            text="Активное упражнение не выбрано.",
            reply_markup=active_workout_keyboard(),
        )
        return

    await api_client.finish_workout_exercise(
        chat_id=query.from_user.id,
        workout_exercise_id=workout_exercise_id,
    )

    context.user_data.pop("workout_exercise_id", None)
    context.user_data.pop("exercise_name", None)
    context.user_data.pop("pending_set", None)

    await query.edit_message_text(
        text="Упражнение завершено. Что дальше?",
        reply_markup=active_workout_keyboard(),
    )


def register_exercise_handlers(application):
    application.add_handler(
        CallbackQueryHandler(exercise_catalog_handler, pattern=r"^exercise:catalog$")
    )
    application.add_handler(
        CallbackQueryHandler(exercise_group_handler, pattern=r"^exercise:group:.+$")
    )
    application.add_handler(
        CallbackQueryHandler(exercise_pick_handler, pattern=r"^exercise:pick:\d+:.+$")
    )
    application.add_handler(
        CallbackQueryHandler(exercise_finish_handler, pattern=r"^exercise:finish$")
    )
