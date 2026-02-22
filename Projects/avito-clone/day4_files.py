# День 4: Работа с файлами в Python

print("=" * 60)
print("РАБОТА С ФАЙЛАМИ")
print("=" * 60)

# --- Запись в файл ---
print("\n--- ЗАПИСЬ В ФАЙЛ ---")

# Открываем файл для записи ('w' — write)
# Если файла нет — создастся, если есть — перезапишется
with open('test.txt', 'w', encoding='utf-8') as file:
    file.write("Привет, мир!\n")
    file.write("Это вторая строка\n")
    file.write("А это третья\n")

print("✅ Файл test.txt создан и заполнен")

# --- Чтение из файла ---
print("\n--- ЧТЕНИЕ ИЗ ФАЙЛА ---")

with open('test.txt', 'r', encoding='utf-8') as file:
    content = file.read()
    print("Содержимое файла целиком:")
    print(content)

# --- Чтение построчно ---
print("\n--- ЧТЕНИЕ ПОСТРОЧНО ---")

with open('test.txt', 'r', encoding='utf-8') as file:
    print("Читаем строки по очереди:")
    for line in file:
        print(f"  → {line.strip()}")  # strip() убирает символ переноса строки

# --- Добавление в конец файла ---
print("\n--- ДОБАВЛЕНИЕ В ФАЙЛ ---")

with open('test.txt', 'a', encoding='utf-8') as file:  # 'a' — append (добавление)
    file.write("Это строка добавлена в конец\n")

print("✅ Строка добавлена")

# Проверим, что добавилось
with open('test.txt', 'r', encoding='utf-8') as file:
    print("Новое содержимое:")
    print(file.read())

# --- Работа с JSON (самое важное для нас!) ---
print("\n--- РАБОТА С JSON ---")
import json

# Словарь (как наши объявления)
ad = {
    "title": "MacBook Pro",
    "price": 120000,
    "category": "Электроника",
    "city": "Москва"
}

print("Исходный словарь:")
print(ad)

# Сохраняем словарь в JSON-файл
with open('ad.json', 'w', encoding='utf-8') as file:
    json.dump(ad, file, ensure_ascii=False, indent=4)

print("✅ Словарь сохранён в ad.json")

# Читаем JSON обратно
with open('ad.json', 'r', encoding='utf-8') as file:
    loaded_ad = json.load(file)

print("Загруженный из файла словарь:")
print(loaded_ad)

# --- Сохранение списка словарей (как наши ads!) ---
print("\n--- СОХРАНЕНИЕ СПИСКА ОБЪЯВЛЕНИЙ ---")

ads_list = [
    {"title": "MacBook", "price": 80000, "city": "Москва"},
    {"title": "Велосипед", "price": 15000, "city": "СПб"},
    {"title": "Диван", "price": 12000, "city": "Казань"}
]

# Сохраняем весь список
with open('ads.json', 'w', encoding='utf-8') as file:
    json.dump(ads_list, file, ensure_ascii=False, indent=4)

print("✅ Список объявлений сохранён в ads.json")

# Загружаем список обратно
with open('ads.json', 'r', encoding='utf-8') as file:
    loaded_ads = json.load(file)

print("Загруженные объявления:")
for i, ad in enumerate(loaded_ads, 1):
    print(f"  {i}. {ad['title']} — {ad['price']} ₽ ({ad['city']})")

print("\n" + "=" * 60)
print("✅ ОСНОВЫ РАБОТЫ С ФАЙЛАМИ ИЗУЧЕНЫ")
print("=" * 60)
