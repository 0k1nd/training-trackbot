from telegram.ext import Application

from app.api.client import BackendApiClient
from app.handlers.body_metrics import register_body_metrics_handlers
from app.handlers.menu import register_menu_handlers
from app.handlers.start import register_start_handlers
from app.settings import BACKEND_API_URL, BOT_API_TOKEN, TELEGRAM_BOT_TOKEN


def main():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    application.bot_data["api_client"] = BackendApiClient(
        base_url=BACKEND_API_URL,
        bot_api_token=BOT_API_TOKEN,
    )

    register_start_handlers(application)
    register_menu_handlers(application)
    register_body_metrics_handlers(application)

    application.run_polling()


if __name__ == "__main__":
    main()
