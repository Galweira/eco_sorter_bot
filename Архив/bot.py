import json
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "8179513289:AAE89mACc9yUr4cgg1lq3NMsuoG10EkqisU"

# Загрузка данных из JSON
with open('recycling_data.json', 'r', encoding='utf-8') as file:
    recycling_data = json.load(file)

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я бот ЭкоСортировщик. Отправь мне маркировку, например, '01 PET', чтобы узнать, как сортировать этот материал!")

# Обработчик для получения информации о маркировке
async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    marking = " ".join(context.args).strip().upper()

    if marking in recycling_data:
        data = recycling_data[marking]
        response = (f"📌 **{marking}** — {data['description']}\n\n"
                    f"✅ **Принимается:**\n- " + "\n- ".join(data['accepted']) + "\n\n"
                    f"❌ **Не принимается:**\n- " + "\n- ".join(data['not_accepted']) + "\n\n"
                    f"⚠️ **Важно:**\n- " + "\n- ".join(data['important']))
    else:
        response = "Я не нашёл информацию по такой маркировке. Проверь корректность ввода."

    await update.message.reply_text(response, parse_mode='Markdown')

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("info", info))

    print("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()
