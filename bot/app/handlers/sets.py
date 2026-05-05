from telegram import Update
from telegram.ext import (
    CallbackQueryHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from app.conversations.states import WorkoutStates
from app.formatters.sets import format_workout_exercise_sets
from app.keyboards.exercises import workout_exercise_keyboard
from app.keyboards.sets import set_difficulty_keyboard


async def set_add_start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    context.user_data["pending_set"] = {}

    await query.edit_message_text("Введите вес в кг или '-' если без веса.")
    return WorkoutStates.ENTER_SET_WEIGHT


async def set_weight_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    raw = update.message.text.strip().replace(",", ".")

    if raw != "-":
        try:
            weight = float(raw)
        except ValueError:
            await update.message.reply_text("Введите число или '-'.")
            return WorkoutStates.ENTER_SET_WEIGHT

        context.user_data["pending_set"]["weight"] = weight

    await update.message.reply_text("Введите количество повторений или '-'.")
    return WorkoutStates.ENTER_SET_REPS


async def set_reps_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    raw = update.message.text.strip()

    if raw != "-":
        try:
            reps = int(raw)
        except ValueError:
            await update.message.reply_text("Введите целое число или '-'.")
            return WorkoutStates.ENTER_SET_REPS

        context.user_data["pending_set"]["reps"] = reps

    pending = context.user_data.get("pending_set", {})

    if pending.get("weight") is None and pending.get("reps") is None:
        await update.message.reply_text("Нужно указать вес или повторения.")
        return WorkoutStates.ENTER_SET_WEIGHT

    await update.message.reply_text(
        text="Выберите сложность:",
        reply_markup=set_difficulty_keyboard(),
    )
    return ConversationHandler.END


async def set_difficulty_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    difficulty = query.data.split(":")[2]
    pending = context.user_data.get("pending_set", {})
    workout_exercise_id = context.user_data.get("workout_exercise_id")
    api_client = context.application.bot_data["api_client"]

    if not workout_exercise_id:
        await query.edit_message_text("Активное упражнение не выбрано.")
        return

    await api_client.add_set(
        chat_id=query.from_user.id,
        workout_exercise_id=workout_exercise_id,
        weight=pending.get("weight"),
        reps=pending.get("reps"),
        difficulty=difficulty,
    )

    context.user_data.pop("pending_set", None)

    data = await api_client.get_workout_exercise_sets(
        chat_id=query.from_user.id,
        workout_exercise_id=workout_exercise_id,
    )

    await query.edit_message_text(
        text=format_workout_exercise_sets(data),
        reply_markup=workout_exercise_keyboard(),
    )


async def set_repeat_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    workout_exercise_id = context.user_data.get("workout_exercise_id")
    api_client = context.application.bot_data["api_client"]

    if not workout_exercise_id:
        await query.edit_message_text("Активное упражнение не выбрано.")
        return

    data = await api_client.get_workout_exercise_sets(
        chat_id=query.from_user.id,
        workout_exercise_id=workout_exercise_id,
    )

    sets = data.get("sets", [])
    if not sets:
        await query.edit_message_text(
            text="Нет последнего подхода для повтора.",
            reply_markup=workout_exercise_keyboard(),
        )
        return

    last_set = sets[-1]

    await api_client.add_set(
        chat_id=query.from_user.id,
        workout_exercise_id=workout_exercise_id,
        weight=last_set.get("weight"),
        reps=last_set.get("reps"),
        difficulty=last_set["difficulty"],
    )

    updated = await api_client.get_workout_exercise_sets(
        chat_id=query.from_user.id,
        workout_exercise_id=workout_exercise_id,
    )

    await query.edit_message_text(
        text=format_workout_exercise_sets(updated),
        reply_markup=workout_exercise_keyboard(),
    )


def build_add_set_conversation():
    return ConversationHandler(
        entry_points=[
            CallbackQueryHandler(set_add_start_handler, pattern=r"^set:add$"),
        ],
        states={
            WorkoutStates.ENTER_SET_WEIGHT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, set_weight_handler),
            ],
            WorkoutStates.ENTER_SET_REPS: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, set_reps_handler),
            ],
        },
        fallbacks=[],
        per_chat=True,
        per_user=True,
    )


def register_set_handlers(application):
    application.add_handler(build_add_set_conversation())
    application.add_handler(
        CallbackQueryHandler(
            set_difficulty_handler, pattern=r"^set:difficulty:(easy|moderate|hard)$"
        )
    )
    application.add_handler(CallbackQueryHandler(set_repeat_handler, pattern=r"^set:repeat$"))
