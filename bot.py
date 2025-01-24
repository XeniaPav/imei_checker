import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()
import requests
from telegram import Update
from asgiref.sync import sync_to_async
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    CallbackContext,
)
from config.settings import TG_TOKEN, API_SANDBOX
from api.models import WhitelistedUsers, Users

TOKEN = TG_TOKEN


async def get_or_create_user(user_id):
    user, created = await sync_to_async(Users.objects.get_or_create)(chat_id=user_id)
    return user, created


async def check_whitelisted(user):
    exists = await sync_to_async(WhitelistedUsers.objects.filter)(chat_id=user)
    return await sync_to_async(exists.exists)()


async def start(update: Update, context: CallbackContext) -> None:
    """создаем пользователя и проверяем наличие юзера в белом листе"""
    user_id = update.message.from_user.id
    user, created = await get_or_create_user(user_id)
    if await check_whitelisted(user.chat_id):
        await update.message.reply_text(
            "Вы в белом списке! Вы можете использовать API."
        )
        await update.message.reply_text("Отправьте IMEI для проверки.")
    else:
        await update.message.reply_text("Вы не в белом списке, доступ к API запрещен.")


async def check_imei_handler(update: Update, context: CallbackContext):
    """Проверка IMEI в Telegram-боте"""
    imei = update.message.text
    token = API_SANDBOX
    try:
        response = requests.post(
            f"http://localhost:8000/api/check-imei", json={"imei": imei, "token": token}
        )

        if response.status_code == 200:
            result = response.json()
            await update.message.reply_text(f"Информация об IMEI: {result}")
        else:
            await update.message.reply_text(
                "Ошибка при проверке IMEI: "
                + response.json().get("error", "Неизвестная ошибка")
            )
    except Exception as e:
        await update.message.reply_text("Ошибка при проверке IMEI: " + str(e))


def main():
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, check_imei_handler)
    )
    application.initialize()  # Добавляем инициализацию
    application.run_polling()  # Запускаем бот


if __name__ == "__main__":
    main()
