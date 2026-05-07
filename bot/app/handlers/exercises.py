from telegram import Update
from telegram.ext import (
    CallbackQueryHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from app.conversations.states import WorkoutStates
from app.formatters.exercises import format_exercise_detail
from app.keyboards.exercises import (
    equipment_select_keyboard,
    exercise_catalog_keyboard,
    exercise_detail_keyboard,
    exercise_group_keyboard,
    exercises_keyboard,
    muscle_select_keyboard,
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


async def exercise_search_start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    await query.edit_message_text("Введите название упражнения для поиска.")
    return WorkoutStates.SEARCH_EXERCISE


async def exercise_search_text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query_text = update.message.text.strip()
    api_client = context.application.bot_data["api_client"]

    exercises = await api_client.search_exercises(
        chat_id=update.effective_user.id,
        query=query_text,
    )

    await update.message.reply_text(
        text="Результаты поиска:" if exercises else "Ничего не найдено.",
        reply_markup=exercises_keyboard(exercises),
    )

    return ConversationHandler.END


async def exercise_detail_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    exercise_id = int(query.data.split(":")[2])
    api_client = context.application.bot_data["api_client"]

    exercise = await api_client.get_exercise(
        chat_id=query.from_user.id,
        exercise_id=exercise_id,
    )

    await query.edit_message_text(
        text=format_exercise_detail(exercise),
        reply_markup=exercise_detail_keyboard(
            exercise_id=exercise["id"],
            equipment=exercise["equipment"],
        ),
    )


async def create_exercise_start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    context.user_data["new_exercise"] = {}
    await query.edit_message_text("Введите название своего упражнения.")
    return WorkoutStates.CREATE_EXERCISE_NAME


async def create_exercise_name_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.message.text.strip()

    if len(name) < 2:
        await update.message.reply_text("Название слишком короткое. Введите минимум 2 символа.")
        return WorkoutStates.CREATE_EXERCISE_NAME

    if len(name) > 100:
        await update.message.reply_text("Название слишком длинное. Максимум — 100 символов.")
        return WorkoutStates.CREATE_EXERCISE_NAME

    context.user_data["new_exercise"]["name"] = name

    await update.message.reply_text(
        text="Выберите основную группу мышц.",
        reply_markup=muscle_select_keyboard(),
    )
    return WorkoutStates.CREATE_EXERCISE_MUSCLE


async def create_exercise_muscle_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    muscle = query.data.split(":")[3]
    context.user_data["new_exercise"]["primary_muscle"] = muscle

    await query.edit_message_text(
        text="Выберите оборудование.",
        reply_markup=equipment_select_keyboard(),
    )
    return WorkoutStates.CREATE_EXERCISE_EQUIPMENT


async def create_exercise_equipment_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    equipment = query.data.split(":")[3]
    payload = context.user_data["new_exercise"]
    api_client = context.application.bot_data["api_client"]

    exercise = await api_client.create_exercise(
        chat_id=query.from_user.id,
        name=payload["name"],
        primary_muscle=payload["primary_muscle"],
        equipment=equipment,
    )

    context.user_data.pop("new_exercise", None)

    await query.edit_message_text(
        text=f"Упражнение создано: {exercise['name']}",
        reply_markup=exercise_detail_keyboard(
            exercise_id=exercise["id"],
            equipment=exercise["equipment"],
        ),
    )

    return ConversationHandler.END


def build_exercise_search_conversation():
    return ConversationHandler(
        entry_points=[
            CallbackQueryHandler(exercise_search_start_handler, pattern=r"^exercise:search$"),
        ],
        states={
            WorkoutStates.SEARCH_EXERCISE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, exercise_search_text_handler),
            ],
        },
        fallbacks=[],
        per_chat=True,
        per_user=True,
    )


def build_create_exercise_conversation():
    return ConversationHandler(
        entry_points=[
            CallbackQueryHandler(create_exercise_start_handler, pattern=r"^exercise:create$"),
        ],
        states={
            WorkoutStates.CREATE_EXERCISE_NAME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, create_exercise_name_handler),
            ],
            WorkoutStates.CREATE_EXERCISE_MUSCLE: [
                CallbackQueryHandler(
                    create_exercise_muscle_handler, pattern=r"^exercise:create:muscle:.+$"
                ),
            ],
            WorkoutStates.CREATE_EXERCISE_EQUIPMENT: [
                CallbackQueryHandler(
                    create_exercise_equipment_handler, pattern=r"^exercise:create:equipment:.+$"
                ),
            ],
        },
        fallbacks=[],
        per_chat=True,
        per_user=True,
    )


def register_exercise_handlers(application):
    application.add_handler(build_exercise_search_conversation())
    application.add_handler(build_create_exercise_conversation())
    application.add_handler(
        CallbackQueryHandler(exercise_detail_handler, pattern=r"^exercise:detail:\d+$")
    )
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
