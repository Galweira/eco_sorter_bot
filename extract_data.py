import fitz  # pymupdf

# Открываем PDF-файл
pdf_path = 'РСО_Николо_Хованское_Переработка.pdf'
doc = fitz.open(pdf_path)

# Извлекаем текст из всех страниц и сохраняем в один текстовый файл
text = ""
for page in doc:
    text += page.get_text()

with open("recycling_data.txt", "w", encoding="utf-8") as file:
    file.write(text)

print("Текст извлечён и сохранён в recycling_data.txt")
