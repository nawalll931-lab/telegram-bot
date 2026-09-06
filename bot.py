import re
import logging
import os
from telegram import Update
from telegram.ext import (
    Application,
    MessageHandler,
    filters,
    ContextTypes,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")

ADMIN_IDS = [123456789]  # غيّرها لمعرفك

URL_PATTERN = re.compile(
    r"(https?://\S+)|(www\.\S+)|(t\.me/\S+)|(\S+\.(com|net|org|io|me|co|xyz|info|biz)\b)",
    re.IGNORECASE,
)

PROMO_KEYWORDS = [
    "اشترك", "قناتي", "ادعمني", "روابط", "تابعوني", "channel",
    "subscribe", "join now", "اربح المال", "استثمر", "شحن رصيد",
]


def contains_link(text: str) -> bool:
    if not text:
        return False
    return bool(URL_PATTERN.search(text))


def contains_promo_keyword(text: str) -> bool:
    if not text:
        return False
    text_lower = text.lower()
    return any(kw.lower() in text_lower for kw in PROMO_KEYWORDS)


async def delete_promo_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.effective_message
    if message is None:
        return

    text = message.text or message.caption or ""

    if message.from_user and message.from_user.id in ADMIN_IDS:
        return

    if contains_link(text) or contains_promo_keyword(text):
        try:
            await message.delete()
            logger.info(f"تم حذف رسالة: {text[:50]}")
        except Exception as e:
            logger.error(f"فشل حذف الرسالة: {e}")


def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(
        MessageHandler(filters.TEXT | filters.CAPTION, delete_promo_messages)
    )
    logger.info("البوت يعمل الآن...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
