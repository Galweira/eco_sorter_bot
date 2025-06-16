import aiosqlite
import asyncio

async def setup_db():
    async with aiosqlite.connect('eco_bot.db') as db:
        # Таблица для вопросов и ответов
        await db.execute('''
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question TEXT NOT NULL,
                correct_answer TEXT NOT NULL,
                wrong_answers TEXT NOT NULL
            )
        ''')

        # Таблица для хранения баллов пользователей
        await db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                score INTEGER DEFAULT 0
            )
        ''')

        # Пример одного вопроса (можешь позже добавить больше)
        await db.execute('''
            INSERT INTO questions (question, correct_answer, wrong_answers) VALUES (
                'Куда отправить прозрачную бутылку с маркировкой 01 PET?',
                'В контейнер для PET - общие бутылки',
                'В контейнер для PET - белые бутылки;В 05 PP;Не перерабатывается'
            )
        ''')

        await db.commit()
        print("База данных создана и готова к использованию!")

asyncio.run(setup_db())
