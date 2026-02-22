#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Менеджер объявлений — простая программа для практики Python
Аналог Avito в миниатюре
"""

# ============================================================
# ИНИЦИАЛИЗАЦИЯ ДАННЫХ
# ============================================================

# Категории товаров
categories = [
    "Электроника",
    "Транспорт",
    "Недвижимость",
    "Одежда",
    "Спорт",
    "Мебель",
    "Услуги"
]

# Наши объявления (список словарей)
ads = [
    {
        "id": 1,
        "title": "MacBook Air M1 256GB",
        "price": 75000,
        "category": "Электроника",
        "city": "Москва",
        "seller": "Алексей",
        "views": 45,
        "is_active": True
    },
    {
        "id": 2,
        "title": "Велосипед горный Stels",
        "price": 15000,
        "category": "Спорт",
        "city": "Санкт-Петербург",
        "seller": "Иван",
        "views": 23,
        "is_active": True
    },
    {
        "id": 3,
        "title": "Диван угловой Ikea",
        "price": 12000,
        "category": "Мебель",
        "city": "Казань",
        "seller": "Мария",
        "views": 12,
        "is_active": False
    },
    {
        "id": 4,
        "title": "iPhone 13 128GB",
        "price": 45000,
        "category": "Электроника",
        "city": "Москва",
        "seller": "Дмитрий",
        "views": 67,
        "is_active": True
    },
    {
        "id": 5,
        "title": "Квартира студия 25м²",
        "price": 5500000,
        "category": "Недвижимость",
        "city": "Москва",
        "seller": "Агентство НДВ",
        "views": 34,
        "is_active": True
    }
]

# ============================================================
# ФУНКЦИИ ДЛЯ РАБОТЫ С ОБЪЯВЛЕНИЯМИ
# ============================================================

def show_all_ads():
    """Показать все активные объявления"""
    print("\n" + "=" * 60)
    print("ВСЕ АКТИВНЫЕ ОБЪЯВЛЕНИЯ")
    print("=" * 60)
    
    count = 0
    for ad in ads:
        if ad["is_active"]:
            count += 1
            print(f"{count}. {ad['title']}")
            print(f"   Цена: {ad['price']:,} ₽".replace(",", " "))
            print(f"   Категория: {ad['category']} | Город: {ad['city']}")
            print(f"   Продавец: {ad['seller']} | Просмотров: {ad['views']}")
            print("-" * 40)
    
    if count == 0:
        print("Нет активных объявлений")
    
    return count

def filter_by_category(category_name):
    """Показать объявления по категории"""
    print(f"\n{'=' * 60}")
    print(f"КАТЕГОРИЯ: {category_name.upper()}")
    print('=' * 60)
    
    found = False
    for ad in ads:
        if ad["category"].lower() == category_name.lower() and ad["is_active"]:
            found = True
            print(f"📌 {ad['title']}")
            print(f"   Цена: {ad['price']:,} ₽".replace(",", " "))
            print(f"   Категория: {ad['category']} | Город: {ad['city']}")
            print(f"   Просмотров: {ad['views']}")
            print("-" * 40)
    
    if not found:
        print(f"В категории '{category_name}' нет активных объявлений")

def filter_by_city(city_name):
    """Показать объявления по городу"""
    print(f"\n{'=' * 60}")
    print(f"ГОРОД: {city_name.upper()}")
    print('=' * 60)
    
    found = False
    for ad in ads:
        if ad["city"].lower() == city_name.lower() and ad["is_active"]:
            found = True
            print(f"📌 {ad['title']}")
            print(f"   Цена: {ad['price']:,} ₽".replace(",", " "))
            print(f"   Категория: {ad['category']} | Город: {ad['city']}")
            print(f"   Просмотров: {ad['views']}")
            print("-" * 40)
    
    if not found:
        print(f"В городе '{city_name}' нет активных объявлений")

def filter_by_price(min_price, max_price):
    """Показать объявления в диапазоне цен"""
    print(f"\n{'=' * 60}")
    print(f"ТОВАРЫ ОТ {min_price:,} ДО {max_price:,} ₽".replace(",", " "))
    print('=' * 60)
    
    found = False
    for ad in ads:
        if min_price <= ad["price"] <= max_price and ad["is_active"]:
            found = True
            print(f"📌 {ad['title']}")
            print(f"   Цена: {ad['price']:,} ₽".replace(",", " "))
            print(f"   Категория: {ad['category']} | Город: {ad['city']}")
            print("-" * 40)
    
    if not found:
        print("Нет товаров в указанном диапазоне цен")

def add_new_ad():
    """Добавить новое объявление"""
    print("\n" + "=" * 60)
    print("ДОБАВЛЕНИЕ НОВОГО ОБЪЯВЛЕНИЯ")
    print("=" * 60)
    
    # Генерируем новый ID (на 1 больше максимального)
    new_id = max(ad["id"] for ad in ads) + 1
    
    # Ввод данных
    title = input("Название товара: ")
    
    # Проверка корректности цены
    while True:
        try:
            price = int(input("Цена (только цифры): "))
            if price <= 0:
                print("Цена должна быть положительной!")
                continue
            break
        except ValueError:
            print("Ошибка! Введите число.")
    
    # Показываем категории
    print("\nДоступные категории:")
    for i, cat in enumerate(categories, 1):
        print(f"  {i}. {cat}")
    
    # Выбор категории
    while True:
        try:
            cat_choice = int(input("Выберите номер категории: "))
            if 1 <= cat_choice <= len(categories):
                category = categories[cat_choice - 1]
                break
            else:
                print(f"Введите число от 1 до {len(categories)}")
        except ValueError:
            print("Ошибка! Введите число.")
    
    city = input("Город: ")
    seller = input("Ваше имя: ")
    
    # Создаем новое объявление
    new_ad = {
        "id": new_id,
        "title": title,
        "price": price,
        "category": category,
        "city": city,
        "seller": seller,
        "views": 0,
        "is_active": True
    }
    
    # Добавляем в список
    ads.append(new_ad)

    # Сохраняем изменения в файл
    save_ads_to_file()
    
    print("\n✅ Объявление успешно добавлено!")
    print(f"ID объявления: {new_id}")

def show_statistics():
    """Показать статистику по объявлениям"""
    print("\n" + "=" * 60)
    print("СТАТИСТИКА")
    print("=" * 60)
    
    total = len(ads)
    active = sum(1 for ad in ads if ad["is_active"])
    total_views = sum(ad["views"] for ad in ads)
    avg_price = sum(ad["price"] for ad in ads) / total
    
    print(f"Всего объявлений: {total}")
    print(f"Активных: {active}")
    print(f"Продано/неактивных: {total - active}")
    print(f"Общее число просмотров: {total_views}")
    print(f"Средняя цена: {avg_price:,.0f} ₽".replace(",", " "))
    
    # Статистика по категориям
    print("\nПо категориям:")
    for cat in categories:
        cat_count = sum(1 for ad in ads if ad["category"] == cat and ad["is_active"])
        if cat_count > 0:
            cat_views = sum(ad["views"] for ad in ads if ad["category"] == cat)
            print(f"  {cat}: {cat_count} объявлений, {cat_views} просмотров")

def search_by_text(search_term):
    """Поиск по тексту в названии"""
    print(f"\n{'=' * 60}")
    print(f"ПОИСК: '{search_term}'")
    print('=' * 60)
    
    found = False
    for ad in ads:
        if search_term.lower() in ad["title"].lower() and ad["is_active"]:
            found = True
            print(f"📌 {ad['title']}")
            print(f"   Цена: {ad['price']:,} ₽".replace(",", " "))
            print(f"   Категория: {ad['category']} | Город: {ad['city']}")
            print("-" * 40)
    
    if not found:
        print(f"По запросу '{search_term}' ничего не найдено")

# ============================================================
# ГЛАВНОЕ МЕНЮ ПРОГРАММЫ
# ============================================================
def show_popular_ads(min_views=50):
    """Показать популярные объявления (с большим числом просмотров)"""
    print(f"\n{'=' * 60}")
    print(f"ПОПУЛЯРНЫЕ ОБЪЯВЛЕНИЯ (>={min_views} просмотров)")
    print('=' * 60)
    
    found = False
    for ad in ads:
        if ad["views"] >= min_views and ad["is_active"]:
            found = True
            print(f"🔥 {ad['title']}")
            print(f"   Цена: {ad['price']:,} ₽".replace(",", " "))
            print(f"   Просмотров: {ad['views']}")
            print(f"   Продавец: {ad['seller']}")
            print("-" * 40)
    
    if not found:
        print(f"Нет объявлений с {min_views}+ просмотрами")

def show_ads_by_seller(seller_name):
    """Показать объявления конкретного продавца"""
    print(f"\n{'=' * 60}")
    print(f"ОБЪЯВЛЕНИЯ ПРОДАВЦА: {seller_name.upper()}")
    print('=' * 60)
    
    found = False
    total_price = 0
    count = 0
    
    for ad in ads:
        if ad["seller"].lower() == seller_name.lower():
            found = True
            count += 1
            total_price += ad["price"]
            status = "✅ Активно" if ad["is_active"] else "❌ Продано"
            print(f"{count}. {ad['title']}")
            print(f"   Цена: {ad['price']:,} ₽".replace(",", " "))
            print(f"   Статус: {status}")
            print(f"   Просмотров: {ad['views']}")
            print("-" * 40)
    
    if found:
        print(f"\n📊 Итого у продавца {seller_name}:")
        print(f"   Объявлений: {count}")
        print(f"   Средняя цена: {total_price/count:,.0f} ₽".replace(",", " "))
    else:
        print(f"Продавец '{seller_name}' не найден")

def show_cheapest_ads(limit=3):
    """Показать самые дешёвые активные объявления"""
    print(f"\n{'=' * 60}")
    print(f"ТОП-{limit} САМЫХ ДЕШЁВЫХ ТОВАРОВ")
    print('=' * 60)
    
    # Фильтруем только активные и сортируем по цене
    active_ads = [ad for ad in ads if ad["is_active"]]
    sorted_ads = sorted(active_ads, key=lambda x: x["price"])[:limit]
    
    for i, ad in enumerate(sorted_ads, 1):
        print(f"{i}. {ad['title']}")
        print(f"   Цена: {ad['price']:,} ₽".replace(",", " "))
        print(f"   Категория: {ad['category']} | {ad['city']}")
        print("-" * 40)

def bulk_price_update(percent):
    """Массовое обновление цен (например, для скидок)"""
    print(f"\n{'=' * 60}")
    print(f"МАССОВОЕ ИЗМЕНЕНИЕ ЦЕН НА {percent}%")
    print('=' * 60)
    
    confirm = input(f"Изменить цены во всех активных объявлениях на {percent}%? (y/n): ")
    
    if confirm.lower() == 'y':
        changed = 0
        for ad in ads:
            if ad["is_active"]:
                old_price = ad["price"]
                ad["price"] = int(ad["price"] * (1 + percent/100))
                print(f"  {ad['title']}: {old_price:,} ₽ → {ad['price']:,} ₽".replace(",", " "))
                changed += 1
        # Сохраняем изменения в файл
                save_ads_to_file()
                print(f"\n✅ Изменено объявлений: {changed}")
    else:
                print("Операция отменена")
# ============================================================
# ФУНКЦИИ ДЛЯ РАБОТЫ С ФАЙЛАМИ
# ============================================================

import json
import os

def save_ads_to_file(filename="ads_data.json"):
    """Сохраняет все объявления в JSON-файл"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            # Сохраняем только нужные данные (без лишнего)
            data_to_save = []
            for ad in ads:
                # Копируем словарь, чтобы случайно не изменить оригинал
                ad_copy = ad.copy()
                data_to_save.append(ad_copy)
            
            json.dump(data_to_save, f, ensure_ascii=False, indent=2)
        print(f"💾 Данные сохранены в файл {filename}")
        return True
    except Exception as e:
        print(f"❌ Ошибка при сохранении: {e}")
        return False

def load_ads_from_file(filename="ads_data.json"):
    """Загружает объявления из JSON-файла"""
    global ads  # будем менять глобальный список ads
    
    if not os.path.exists(filename):
        print(f"📁 Файл {filename} не найден. Начинаем с пустого списка.")
        return False
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            loaded_data = json.load(f)
        
        # Проверяем, что загрузили список
        if isinstance(loaded_data, list):
            ads = loaded_data
            print(f"📂 Загружено {len(ads)} объявлений из файла {filename}")
            return True
        else:
            print(f"❌ Ошибка: файл {filename} содержит не список")
            return False
    except Exception as e:
        print(f"❌ Ошибка при загрузке: {e}")
        return False
def create_sample_data():
    """Создаёт тестовые объявления для первого запуска"""
    global ads
    ads = [
        {
            "id": 1,
            "title": "MacBook Air M1 256GB",
            "price": 75000,
            "category": "Электроника",
            "city": "Москва",
            "seller": "Алексей",
            "views": 45,
            "is_active": True
        },
        {
            "id": 2,
            "title": "Велосипед горный Stels",
            "price": 15000,
            "category": "Спорт",
            "city": "Санкт-Петербург",
            "seller": "Иван",
            "views": 23,
            "is_active": True
        },
        {
            "id": 3,
            "title": "Диван угловой Ikea",
            "price": 12000,
            "category": "Мебель",
            "city": "Казань",
            "seller": "Мария",
            "views": 12,
            "is_active": False
        }
    ]
    print("📦 Созданы тестовые объявления")
    save_ads_to_file()  # сразу сохраняем в файл
def main():
    """Главная функция программы"""
    
    print("=" * 60)
    print("🏠 МЕНЕДЖЕР ОБЪЯВЛЕНИЙ v1.0")
    print("=" * 60)
    print("Добро пожаловать в систему управления объявлениями!")
    
    while True:
        print("\n" + "-" * 40)
        print("ГЛАВНОЕ МЕНЮ:")
        print("  1. Показать все объявления")
        print("  2. Поиск по категории")
        print("  3. Поиск по городу")
        print("  4. Поиск по цене")
        print("  5. Поиск по тексту")
        print("  6. Добавить объявление")
        print("  7. Статистика")
        print("  8. Популярные объявления")
        print("  9. Объявления продавца")
        print(" 10. Топ самых дешёвых")
        print(" 11. Массовое изменение цен")
        print(" 12. Сохранить данные вручную")
        print("  0. Выход")
        print("-" * 40)
        
        choice = input("Выберите действие (0-11): ").strip()
        
        if choice == "1":
            show_all_ads()
        
        elif choice == "2":
            print("\nДоступные категории:")
            for i, cat in enumerate(categories, 1):
                print(f"  {i}. {cat}")
            cat_name = input("Введите название категории: ").strip()
            if cat_name:
                filter_by_category(cat_name)
            else:
                print("Категория не указана")
        
        elif choice == "3":
            city = input("Введите название города: ").strip()
            if city:
                filter_by_city(city)
            else:
                print("Город не указан")
        
        elif choice == "4":
            try:
                min_p = int(input("Минимальная цена: "))
                max_p = int(input("Максимальная цена: "))
                if min_p <= max_p:
                    filter_by_price(min_p, max_p)
                else:
                    print("Минимальная цена должна быть меньше максимальной")
            except ValueError:
                print("Ошибка! Введите числа")
        
        elif choice == "5":
            text = input("Введите текст для поиска: ").strip()
            if text:
                search_by_text(text)
            else:
                print("Текст не указан")
        
        elif choice == "6":
            add_new_ad()
        
        elif choice == "7":
            show_statistics()
        
        elif choice == "8":
            try:
                min_views = input("Минимальное число просмотров (Enter для 50): ")
                if min_views.strip() == "":
                    show_popular_ads()
                else:
                    show_popular_ads(int(min_views))
            except ValueError:
                print("Ошибка! Введите число")
        
        elif choice == "9":
            seller = input("Введите имя продавца: ").strip()
            if seller:
                show_ads_by_seller(seller)
            else:
                print("Имя продавца не указано")
        
        elif choice == "10":
            try:
                limit = input("Сколько показать? (Enter для 3): ")
                if limit.strip() == "":
                    show_cheapest_ads()
                else:
                    show_cheapest_ads(int(limit))
            except ValueError:
                print("Ошибка! Введите число")
        
        elif choice == "11":
            try:
                percent = float(input("Введите процент изменения (например, -10 для скидки 10%): "))
                bulk_price_update(percent)
            except ValueError:
                print("Ошибка! Введите число")
        
        elif choice == "12":
            save_ads_to_file()
        
        elif choice == "0":
            print("\nСпасибо за использование программы! До свидания!")
            break
        
        else:
            print("Неверный выбор. Попробуйте снова.")
        
        input("\nНажмите Enter, чтобы продолжить...")        
# ============================================================
# Загружаем данные при старте
# Загружаем данные при старте
if not load_ads_from_file():
    create_sample_data()
if __name__ == "__main__":
    main()
