import re
import json

# Читаем извлечённый текст
with open('recycling_data.txt', 'r', encoding='utf-8') as file:
    text = file.read()

# Ищем фракции (номера маркировок)
pattern = re.compile(r'(\d{2}\s?[A-Z]+|07 OTHER)\s*(.+?)\n(✔.+?)(×.+?)(!.*?)(?=\n\d{2}|$)', re.DOTALL)
matches = pattern.findall(text)

data = {}

for match in matches:
    marking, description, accepted, not_accepted, important = match

    # Очистка и структурирование данных
    marking = marking.strip()
    description = description.strip()

    accepted_list = [item.strip('✔ ').strip() for item in accepted.split('✔') if item.strip()]
    not_accepted_list = [item.strip('× ').strip() for item in not_accepted.split('×') if item.strip()]
    important_list = [item.strip('! ').strip() for item in important.split('!') if item.strip()]

    data[marking] = {
        "description": description,
        "accepted": accepted_list,
        "not_accepted": not_accepted_list,
        "important": important_list
    }

# Сохраняем в JSON-файл
with open('recycling_data.json', 'w', encoding='utf-8') as json_file:
    json.dump(data, json_file, ensure_ascii=False, indent=4)

print("Данные структурированы и сохранены в recycling_data.json")
