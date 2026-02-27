# День 2: Переменные и типы данных для объявлений

print("=" * 50)
print("ПЕРЕМЕННЫЕ И ТИПЫ ДАННЫХ")
print("=" * 50)

# --- Числа (int, float) ---
print("\n--- ЧИСЛА ---")
# int - целые числа
price = 50000
views = 125
print(f"Цена объявления: {price} ₽ (тип: {type(price)})")
print(f"Количество просмотров: {views} (тип: {type(views)})")

# float - числа с плавающей точкой (дробные)
rating = 4.75
discount = 0.15
print(f"Рейтинг продавца: {rating} (тип: {type(rating)})")
print(f"Скидка: {discount * 100}% (тип: {type(discount)})")

# Арифметические операции
new_price = price * (1 - discount)  # цена со скидкой
print(f"Цена со скидкой: {new_price} ₽")

# --- Строки (str) ---
print("\n--- СТРОКИ ---")
title = "MacBook Air M1 в отличном состоянии"
description = 'Продаю свой MacBook, покупал в 2023 году'
city = "Москва"

print(f"Заголовок: {title}")
print(f"Описание: {description}")
print(f"Город: {city}")
print(f"Тип заголовка: {type(title)}")

# Операции со строками
print(f"Длина заголовка: {len(title)} символов")
print(f"Заголовок в верхнем регистре: {title.upper()}")
print(f"Содержит 'MacBook'? {'MacBook' in title}")

# --- Булевы значения (bool) ---
print("\n--- БУЛЕВЫ ЗНАЧЕНИЯ ---")
is_active = True
is_sold = False
is_featured = True  # выделенное объявление

print(f"Активно: {is_active} (тип: {type(is_active)})")
print(f"Продано: {is_sold} (тип: {type(is_sold)})")
print(f"Выделено: {is_featured}")

# Логические операции
can_be_shown = is_active and not is_sold  # активно И НЕ продано
print(f"Может показываться: {can_be_shown}")

# Сравнения
min_price = 10000
print(f"Цена >= 10000? {price >= min_price}")

# --- None — ничего/пусто ---
print("\n--- NONE (пустое значение) ---")
phone = None  # телефон не указан
sold_date = None  # дата продажи неизвестна
print(f"Телефон: {phone} (тип: {type(phone)})")
print(f"Дата продажи: {sold_date}")

print("\n--- МОЯ ПРАКТИКА ---")
# Создайте переменные для вашего объявления:
# 1. Название товара (строка)
# 2. Цена (число)
# 3. Есть ли доставка (булево значение)
# 4. Рейтинг продавца (дробное число)
# 5. Адрес (строка или None, если не указан)

# Напишите код здесь:
my_title = "iPhone 16 pro max"
my_price = 90000
has_delivery = True
seller_rating = 4.9
address = None

# Выведите все переменные
print(f"Товар: {my_title}")
print(f"Цена: {my_price} ₽")
print(f"Доставка: {'есть' if has_delivery else 'нет'}")
print(f"Рейтинг: {seller_rating}")
print(f"Адрес: {address if address else 'не указан'}"
print("\n" + "=" * 50)
print("СПИСКИ (list)")
print("=" * 50)

# Список — упорядоченная коллекция элементов
print("\n--- СОЗДАНИЕ СПИСКОВ ---")

# Список категорий
categories = ["Электроника", "Одежда", "Недвижимость", "Транспорт"]
print(f"Категории: {categories}")
print(f"Тип: {type(categories)}")
print(f"Количество категорий: {len(categories)}")

# Список цен на похожие товары
similar_prices = [45000, 52000, 38000, 49000]
print(f"Цены похожих товаров: {similar_prices}")

# Смешанный список (так можно, но лучше не смешивать типы)
mixed = ["iPhone", 50000, True]
print(f"Смешанный список: {mixed}")

print("\n--- РАБОТА СО СПИСКАМИ ---")
# Доступ по индексу (счет с 0!)
first_category = categories[0]  # первый элемент
last_category = categories[-1]  # последний элемент
print(f"Первая категория: {first_category}")
print(f"Последняя категория: {last_category}")

# Срезы
first_two = categories[0:2]  # первые два элемента
print(f"Первые две категории: {first_two}")

# Изменение элементов
categories[1] = "Одежда и обувь"
print(f"После изменения: {categories}")

# Добавление элементов
categories.append("Услуги")
print(f"После добавления: {categories}")

# Удаление элементов
removed = categories.pop(2)  # удаляем элемент с индексом 2
print(f"Удалено: {removed}")
print(f"После удаления: {categories}")

# Перебор списка циклом
print("\n--- ПЕРЕБОР СПИСКА ---")
for category in categories:
    print(f"- {category}")

print("\n" + "=" * 50)
print("СЛОВАРИ (dict)")
print("=" * 50)

# Словарь — коллекция пар ключ-значение
print("\n--- СОЗДАНИЕ СЛОВАРЕЙ ---")

# Одно объявление как словарь
ad1 = {
    "title": "MacBook Air M1",
    "price": 80000,
    "category": "Электроника",
    "is_active": True,
    "views": 125,
    "seller_rating": 4.8
}

print(f"Объявление: {ad1}")
print(f"Тип: {type(ad1)}")
print(f"Количество полей: {len(ad1)}")

print("\n--- ДОСТУП К ЗНАЧЕНИЯМ ---")
print(f"Название: {ad1['title']}")
print(f"Цена: {ad1['price']} ₽")
print(f"Категория: {ad1['category']}")

# Безопасный доступ (не вызовет ошибку, если ключа нет)
rating = ad1.get("seller_rating", "нет рейтинга")
print(f"Рейтинг (через get): {rating}")

print("\n--- ИЗМЕНЕНИЕ СЛОВАРЕЙ ---")
# Добавление нового поля
ad1["city"] = "Москва"
print(f"После добавления города: {ad1}")

# Изменение существующего поля
ad1["price"] = 75000
print(f"После изменения цены: {ad1}")

# Удаление поля
ad1.pop("views", None)  # удаляем просмотры
print(f"После удаления views: {ad1}")

print("\n--- ПЕРЕБОР СЛОВАРЯ ---")
print("Все поля объявления:")
for key, value in ad1.items():
    print(f"  {key}: {value}")

print("\n--- СПИСОК СЛОВАРЕЙ (наши объявления) ---")
# Вот как мы будем хранить множество объявлений!
ads = [
    {
        "title": "MacBook Air M1",
        "price": 80000,
        "category": "Электроника",
        "city": "Москва"
    },
    {
        "title": "Велосипед Stels",
        "price": 15000,
        "category": "Спорт",
        "city": "СПб"
    },
    {
        "title": "Диван Ikea",
        "price": 12000,
        "category": "Мебель",
        "city": "Казань"
    }
]

print(f"Всего объявлений: {len(ads)}")
print("\nСписок объявлений:")
for i, ad in enumerate(ads, 1):
    print(f"  {i}. {ad['title']} - {ad['price']} ₽ ({ad['city']})")

