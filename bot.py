import json
import random
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import aiosqlite

TOKEN = "8179513289:AAE89mACc9yUr4cgg1lq3NMsuoG10EkqisU"

# Загрузка данных JSON
with open('recycling_data.json', 'r', encoding='utf-8') as file:
    recycling_data = json.load(file)

# Функция главного меню (выше остальных, примерно 12-я строка)
async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    main_menu_buttons = [
        ["📝 Пройти тест", "🔎 Узнать о маркировке"],
        ["📚 Шпаргалка по маркировкам", "🏆 Рейтинг пользователей"]
    ]
    reply_markup = ReplyKeyboardMarkup(main_menu_buttons, resize_keyboard=True)
    await update.message.reply_text(
        "♻️ Добро пожаловать в ЭкоСортировщик! Выберите действие:",
        reply_markup=reply_markup
    )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await show_main_menu(update, context)

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    marking = " ".join(context.args).strip().upper()
    if marking in recycling_data:
        data = recycling_data[marking]
        response = f"♻️ **{marking} — {data['description']}**\n\n"
        response += "✅ **Принимается:**\n- " + "\n- ".join(data['accepted']) + "\n\n"
        response += "❌ **Не принимается:**\n- " + "\n- ".join(data['not_accepted']) + "\n\n"
        response += "⚠️ **Важно:**\n- " + "\n- ".join(data['important'])
    else:
        response = "Не удалось найти информацию по такой маркировке."

    await update.message.reply_text(response, parse_mode='Markdown')

async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    async with aiosqlite.connect('eco_bot.db') as db:
        cursor = await db.execute('SELECT * FROM questions ORDER BY RANDOM() LIMIT 1')
        question = await cursor.fetchone()

    correct_answer = question[2]
    wrong_answers = question[3].split(';')

    options = wrong_answers + [correct_answer, "↩️ Главное меню"]
    random.shuffle(options)

    context.user_data['correct_answer'] = correct_answer

    await update.message.reply_text(
        question[1],
        reply_markup=ReplyKeyboardMarkup([options], one_time_keyboard=True, resize_keyboard=True)
    )

async def handle_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_answer = update.message.text
    correct_answer = context.user_data.get('correct_answer')

    if user_answer == "↩️ Главное меню":
        await show_main_menu(update, context)
        return

    async with aiosqlite.connect('eco_bot.db') as db:
        if user_answer == correct_answer:
            await update.message.reply_text("🎉 Правильно! Ты получаешь 1 балл.", reply_markup=ReplyKeyboardRemove())
            user_id = update.message.from_user.id
            username = update.message.from_user.username
            await db.execute(
                'INSERT OR IGNORE INTO users (user_id, username, score) VALUES (?, ?, 0)', 
                (user_id, username)
            )
            await db.execute('UPDATE users SET score = score + 1 WHERE user_id = ?', (user_id,))
            await db.commit()
        else:
            await update.message.reply_text(f"❌ Неправильно. Правильный ответ: {correct_answer}", reply_markup=ReplyKeyboardRemove())

async def leaderboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    async with aiosqlite.connect('eco_bot.db') as db:
        cursor = await db.execute('SELECT username, score FROM users ORDER BY score DESC LIMIT 10')
        top_users = await cursor.fetchall()

    leaderboard_text = "🏆 **Топ игроков:**\n"
    for i, (username, score) in enumerate(top_users, start=1):
        leaderboard_text += f"{i}. @{username or 'аноним'} — {score} баллов\n"

    markup = ReplyKeyboardMarkup([["↩️ Главное меню"]], resize_keyboard=True)
    await update.message.reply_text(leaderboard_text, reply_markup=markup, parse_mode='Markdown')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = "📌 **Шпаргалка по маркировкам:**\n\n"
    for marking, data in recycling_data.items():
        help_text += f"**{marking}** — {data['description']}\n"
    markup = ReplyKeyboardMarkup([["↩️ Главное меню"]], resize_keyboard=True)
    await update.message.reply_text(help_text, reply_markup=markup, parse_mode='Markdown')

async def handle_main_menu_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "📝 Пройти тест":
        await quiz(update, context)
    elif text == "🔎 Узнать о маркировке":
        await prompt_info(update, context)
    elif text == "📚 Шпаргалка по маркировкам":
        await help_command(update, context)
    elif text == "🏆 Рейтинг пользователей":
        await leaderboard(update, context)
    else:
        await update.message.reply_text("Выберите действие из меню.")

async def prompt_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    markup = ReplyKeyboardMarkup(
        [["01 PET", "02 HDPE", "04 LDPE"], ["05 PP", "07 OTHER", "40 FE"], ["↩️ Главное меню"]],
        resize_keyboard=True
    )
    await update.message.reply_text("Выберите маркировку или введите вручную:", reply_markup=markup)

async def handle_marking(update: Update, context: ContextTypes.DEFAULT_TYPE):
    marking = update.message.text.strip().upper()

    if marking == "↩️ ГЛАВНОЕ МЕНЮ":
        await show_main_menu(update, context)
        return

    if marking in recycling_data:
        data = recycling_data[marking]
        response = f"♻️ **{marking} — {data['description']}**\n\n"
        response += "✅ **Принимается:**\n- " + "\n- ".join(data['accepted']) + "\n\n"
        response += "❌ **Не принимается:**\n- " + "\n- ".join(data['not_accepted']) + "\n\n"
        response += "⚠️ **Важно:**\n- " + "\n- ".join(data['important'])
    else:
        response = "Не удалось найти информацию по такой маркировке."

    await update.message.reply_text(response, parse_mode='Markdown')

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("info", info))
    app.add_handler(CommandHandler("quiz", quiz))
    app.add_handler(CommandHandler("leaderboard", leaderboard))
    app.add_handler(CommandHandler("help", help_command))

    app.add_handler(MessageHandler(filters.Regex('^(📝 Пройти тест|🔎 Узнать о маркировке|📚 Шпаргалка по маркировкам|🏆 Рейтинг пользователей)$'), handle_main_menu_buttons))
    app.add_handler(MessageHandler(filters.Regex('^↩️ Главное меню$'), show_main_menu))
    app.add_handler(MessageHandler(filters.Regex(r'^\d{2}\s?[A-Z]+$'), handle_marking))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_answer))

    print("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()
