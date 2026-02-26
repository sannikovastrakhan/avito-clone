#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Менеджер объявлений — версия с PostgreSQL
"""

import psycopg2
from psycopg2 import sql, extras
from tabulate import tabulate
from datetime import datetime, timedelta

# ============================================================
# ПОДКЛЮЧЕНИЕ К БАЗЕ ДАННЫХ
# ============================================================

class AdManager:
    def __init__(self, dbname="avito_clone", user=None):
        """Инициализация подключения к БД"""
        if user is None:
            import getpass
            user = getpass.getuser()
        
        self.conn_params = {
            "dbname": dbname,
            "user": user,
            "host": "localhost"
        }
        self.conn = None
        self.connect()
    
    def connect(self):
        """Установка соединения с БД"""
        try:
            self.conn = psycopg2.connect(**self.conn_params)
            print("✅ Подключено к базе данных")
        except Exception as e:
            print(f"❌ Ошибка подключения: {e}")
            print("💡 Убедитесь, что PostgreSQL запущен: brew services start postgresql@15")
            exit(1)
    
    def close(self):
        """Закрытие соединения"""
        if self.conn:
            self.conn.close()
            print("👋 Соединение с БД закрыто")
    
    # ============================================================
    # ФУНКЦИИ ДЛЯ РАБОТЫ С ОБЪЯВЛЕНИЯМИ
    # ============================================================
    
    def show_all_ads(self):
        """Показать все активные объявления"""
        with self.conn.cursor(cursor_factory=extras.RealDictCursor) as cur:
            cur.execute("""
                SELECT a.*, c.name as category_name 
                FROM ads a
                JOIN categories c ON a.category_id = c.id
                WHERE a.is_active = true
                ORDER BY a.created_at DESC
            """)
            ads = cur.fetchall()
            
            print("\n" + "=" * 60)
            print("ВСЕ АКТИВНЫЕ ОБЪЯВЛЕНИЯ")
            print("=" * 60)
            
            if not ads:
                print("Нет активных объявлений")
                return
            
            for ad in ads:
                print(f"📌 {ad['title']}")
                print(f"   Цена: {ad['price']:,} ₽".replace(",", " "))
                print(f"   Категория: {ad['category_name']} | Город: {ad['city']}")
                print(f"   Продавец: {ad['seller']} | Просмотров: {ad['views']}")
                print("-" * 40)
    
    def add_new_ad(self):
        """Добавить новое объявление"""
        print("\n" + "=" * 60)
        print("ДОБАВЛЕНИЕ НОВОГО ОБЪЯВЛЕНИЯ")
        print("=" * 60)
        
        # Получаем список категорий из БД
        with self.conn.cursor(cursor_factory=extras.RealDictCursor) as cur:
            cur.execute("SELECT id, name FROM categories ORDER BY name")
            categories = cur.fetchall()
        
        print("\nДоступные категории:")
        for cat in categories:
            print(f"  {cat['id']}. {cat['name']}")
        
        # Ввод данных
        title = input("Название товара: ")
        
        while True:
            try:
                price = int(input("Цена (только цифры): "))
                if price <= 0:
                    print("Цена должна быть положительной!")
                    continue
                break
            except ValueError:
                print("Ошибка! Введите число.")
        
        while True:
            try:
                cat_id = int(input("Выберите номер категории: "))
                if any(cat['id'] == cat_id for cat in categories):
                    break
                else:
                    print("Неверный номер категории")
            except ValueError:
                print("Ошибка! Введите число.")
        
        city = input("Город: ")
        seller = input("Ваше имя: ")
        
        # Сохраняем в БД
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO ads (title, price, category_id, city, seller, views)
                VALUES (%s, %s, %s, %s, %s, 0)
                RETURNING id
            """, (title, price, cat_id, city, seller))
            
            new_id = cur.fetchone()[0]
            self.conn.commit()
            
            print(f"\n✅ Объявление успешно добавлено! ID: {new_id}")
    
    def show_statistics(self):
        """Показать статистику"""
        with self.conn.cursor(cursor_factory=extras.RealDictCursor) as cur:
            # Общая статистика
            cur.execute("""
                SELECT 
                    COUNT(*) as total,
                    SUM(CASE WHEN is_active THEN 1 ELSE 0 END) as active,
                    SUM(views) as total_views,
                    AVG(price) as avg_price
                FROM ads
            """)
            stats = cur.fetchone()
            
            print("\n" + "=" * 60)
            print("СТАТИСТИКА")
            print("=" * 60)
            print(f"Всего объявлений: {stats['total']}")
            print(f"Активных: {stats['active']}")
            print(f"Общее число просмотров: {stats['total_views']}")
            print(f"Средняя цена: {stats['avg_price']:,.0f} ₽".replace(",", " "))
            
            # Статистика по категориям
            cur.execute("""
                SELECT 
                    c.name,
                    COUNT(a.id) as ads_count,
                    SUM(a.views) as views_count
                FROM categories c
                LEFT JOIN ads a ON c.id = a.category_id AND a.is_active = true
                GROUP BY c.name
                HAVING COUNT(a.id) > 0
            """)
            
            print("\nПо категориям:")
            for row in cur.fetchall():
                print(f"  {row['name']}: {row['ads_count']} объявлений, {row['views_count'] or 0} просмотров")
    
    # ============================================================
    # ГЛАВНОЕ МЕНЮ
    # ============================================================
    # ============================================================
    # НОВЫЕ ФУНКЦИИ ДНЯ 6
    # ============================================================
    
    def search_ads(self):
        """Поиск объявлений по разным критериям"""
        print("\n" + "=" * 60)
        print("ПОИСК ОБЪЯВЛЕНИЙ")
        print("=" * 60)
        print("1. Поиск по названию")
        print("2. Поиск по цене")
        print("3. Поиск по городу")
        print("4. Поиск по категории")
        print("0. Назад")
        
        choice = input("\nВыберите тип поиска: ").strip()
        
        with self.conn.cursor(cursor_factory=extras.RealDictCursor) as cur:
            if choice == "1":
                term = input("Введите текст для поиска: ").strip()
                cur.execute("""
                    SELECT a.*, c.name as category_name 
                    FROM ads a
                    JOIN categories c ON a.category_id = c.id
                    WHERE a.is_active = true 
                      AND a.title ILIKE %s
                    ORDER BY a.price
                """, (f'%{term}%',))
                
            elif choice == "2":
                try:
                    min_p = int(input("Минимальная цена: "))
                    max_p = int(input("Максимальная цена: "))
                    cur.execute("""
                        SELECT a.*, c.name as category_name 
                        FROM ads a
                        JOIN categories c ON a.category_id = c.id
                        WHERE a.is_active = true 
                          AND a.price BETWEEN %s AND %s
                        ORDER BY a.price
                    """, (min_p, max_p))
                except ValueError:
                    print("Ошибка! Введите числа")
                    return
                    
            elif choice == "3":
                city = input("Введите город: ").strip()
                cur.execute("""
                    SELECT a.*, c.name as category_name 
                    FROM ads a
                    JOIN categories c ON a.category_id = c.id
                    WHERE a.is_active = true 
                      AND a.city ILIKE %s
                    ORDER BY a.price
                """, (f'%{city}%',))
                
            elif choice == "4":
                # Получаем список категорий
                cur.execute("SELECT id, name FROM categories ORDER BY name")
                categories = cur.fetchall()
                print("\nДоступные категории:")
                for cat in categories:
                    print(f"  {cat['id']}. {cat['name']}")
                
                try:
                    cat_id = int(input("Выберите номер категории: "))
                    cur.execute("""
                        SELECT a.*, c.name as category_name 
                        FROM ads a
                        JOIN categories c ON a.category_id = c.id
                        WHERE a.is_active = true 
                          AND a.category_id = %s
                        ORDER BY a.price
                    """, (cat_id,))
                except ValueError:
                    print("Ошибка! Введите число")
                    return
            else:
                return
            
            results = cur.fetchall()
            
            if not results:
                print("\n❌ Ничего не найдено")
                return
            
            print(f"\n📋 Найдено объявлений: {len(results)}")
            print("-" * 60)
            for ad in results:
                print(f"📌 {ad['title']}")
                print(f"   Цена: {ad['price']:,} ₽".replace(",", " "))
                print(f"   Категория: {ad['category_name']} | Город: {ad['city']}")
                print(f"   Продавец: {ad['seller']} | Просмотров: {ad['views']}")
                print("-" * 40)
    
    def update_ad(self):
        """Обновление существующего объявления"""
        print("\n" + "=" * 60)
        print("РЕДАКТИРОВАНИЕ ОБЪЯВЛЕНИЯ")
        print("=" * 60)
        
        try:
            ad_id = int(input("Введите ID объявления: "))
        except ValueError:
            print("Ошибка! Введите число")
            return
        
        # Проверяем, существует ли объявление
        with self.conn.cursor(cursor_factory=extras.RealDictCursor) as cur:
            cur.execute("SELECT * FROM ads WHERE id = %s", (ad_id,))
            ad = cur.fetchone()
            
            if not ad:
                print(f"❌ Объявление с ID {ad_id} не найдено")
                return
            
            print(f"\nТекущие данные:")
            print(f"Название: {ad['title']}")
            print(f"Цена: {ad['price']} ₽")
            print(f"Статус: {'Активно' if ad['is_active'] else 'Неактивно'}")
            
            print("\nЧто хотите изменить?")
            print("1. Название")
            print("2. Цену")
            print("3. Статус (активно/неактивно)")
            print("0. Отмена")
            
            choice = input("Выберите действие: ").strip()
            
            if choice == "1":
                new_title = input("Новое название: ").strip()
                if new_title:
                    cur.execute("UPDATE ads SET title = %s WHERE id = %s", (new_title, ad_id))
                    self.conn.commit()
                    print("✅ Название обновлено!")
                    
            elif choice == "2":
                try:
                    new_price = int(input("Новая цена: "))
                    if new_price > 0:
                        cur.execute("UPDATE ads SET price = %s WHERE id = %s", (new_price, ad_id))
                        self.conn.commit()
                        print("✅ Цена обновлена!")
                    else:
                        print("Цена должна быть положительной")
                except ValueError:
                    print("Ошибка! Введите число")
                    
            elif choice == "3":
                new_status = not ad['is_active']
                cur.execute("UPDATE ads SET is_active = %s WHERE id = %s", (new_status, ad_id))
                self.conn.commit()
                print(f"✅ Статус изменён на {'Активно' if new_status else 'Неактивно'}!")
    
    def delete_ad(self):
        """Удаление объявления (мягкое удаление)"""
        print("\n" + "=" * 60)
        print("УДАЛЕНИЕ ОБЪЯВЛЕНИЯ")
        print("=" * 60)
        
        try:
            ad_id = int(input("Введите ID объявления для удаления: "))
        except ValueError:
            print("Ошибка! Введите число")
            return
        
        # Проверяем существование
        with self.conn.cursor(cursor_factory=extras.RealDictCursor) as cur:
            cur.execute("SELECT title FROM ads WHERE id = %s", (ad_id,))
            ad = cur.fetchone()
            
            if not ad:
                print(f"❌ Объявление с ID {ad_id} не найдено")
                return
            
            confirm = input(f"Удалить объявление '{ad['title']}'? (y/n): ")
            
            if confirm.lower() == 'y':
                # Мягкое удаление — просто деактивируем
                cur.execute("UPDATE ads SET is_active = false WHERE id = %s", (ad_id,))
                self.conn.commit()
                print("✅ Объявление деактивировано!")
            else:
                print("Операция отменена")
    
    def show_top_ads(self):
        """Показать топ объявлений"""
        print("\n" + "=" * 60)
        print("ТОП ОБЪЯВЛЕНИЙ")
        print("=" * 60)
        print("1. Самые дорогие")
        print("2. Самые популярные (по просмотрам)")
        print("3. Самые дешёвые")
        
        choice = input("\nВыберите: ").strip()
        
        with self.conn.cursor(cursor_factory=extras.RealDictCursor) as cur:
            if choice == "1":
                cur.execute("""
                    SELECT a.*, c.name as category_name 
                    FROM ads a
                    JOIN categories c ON a.category_id = c.id
                    WHERE a.is_active = true
                    ORDER BY a.price DESC
                    LIMIT 5
                """)
            elif choice == "2":
                cur.execute("""
                    SELECT a.*, c.name as category_name 
                    FROM ads a
                    JOIN categories c ON a.category_id = c.id
                    WHERE a.is_active = true
                    ORDER BY a.views DESC
                    LIMIT 5
                """)
            elif choice == "3":
                cur.execute("""
                    SELECT a.*, c.name as category_name 
                    FROM ads a
                    JOIN categories c ON a.category_id = c.id
                    WHERE a.is_active = true
                    ORDER BY a.price
                    LIMIT 5
                """)
            else:
                return
            
            results = cur.fetchall()
            
            if not results:
                print("\nНет данных")
                return
            
            print("\n" + "-" * 60)
            for i, ad in enumerate(results, 1):
                print(f"{i}. {ad['title']}")
                print(f"   Цена: {ad['price']:,} ₽ | Просмотров: {ad['views']}")
                print(f"   Категория: {ad['category_name']} | {ad['city']}")
                print("-" * 40)
    # ============================================================
    # НОВЫЕ ФУНКЦИИ ДНЯ 7
    # ============================================================
    
    def show_time_stats(self):
        """Статистика по времени создания объявлений"""
        print("\n" + "=" * 60)
        print("СТАТИСТИКА ПО ВРЕМЕНИ")
        print("=" * 60)
        
        with self.conn.cursor(cursor_factory=extras.RealDictCursor) as cur:
            # Статистика по дням
            cur.execute("""
                SELECT 
                    DATE(created_at) as date,
                    COUNT(*) as new_ads,
                    SUM(views) as daily_views
                FROM ads
                GROUP BY date
                ORDER BY date DESC
                LIMIT 10
            """)
            
            daily_stats = cur.fetchall()
            
            if daily_stats:
                print("\n📅 Последние 10 дней:")
                # Готовим данные для таблицы
                table_data = []
                for stat in daily_stats:
                    table_data.append([
                        stat['date'].strftime('%Y-%m-%d'),
                        stat['new_ads'],
                        stat['daily_views'] or 0
                    ])
                
                print(tabulate(
                    table_data,
                    headers=['Дата', 'Новых', 'Просмотров'],
                    tablefmt='grid'
                ))
            
            # Среднее время жизни объявления
            cur.execute("""
                SELECT 
                    AVG(EXTRACT(DAY FROM (NOW() - created_at))) as avg_days
                FROM ads
                WHERE is_active = true
            """)
            avg_days = cur.fetchone()['avg_days']
            if avg_days:
                print(f"\n📊 Среднее время жизни активного объявления: {avg_days:.1f} дней")
    
    def show_category_chart(self):
        """Показать график распределения по категориям"""
        print("\n" + "=" * 60)
        print("РАСПРЕДЕЛЕНИЕ ПО КАТЕГОРИЯМ")
        print("=" * 60)
        
        with self.conn.cursor(cursor_factory=extras.RealDictCursor) as cur:
            cur.execute("""
                SELECT 
                    c.name,
                    COUNT(a.id) as ads_count
                FROM categories c
                LEFT JOIN ads a ON c.id = a.category_id AND a.is_active = true
                GROUP BY c.name
                HAVING COUNT(a.id) > 0
                ORDER BY ads_count DESC
            """)
            
            categories = cur.fetchall()
            
            if not categories:
                print("Нет данных")
                return
            
            # Находим максимальное количество для масштабирования
            max_count = max(cat['ads_count'] for cat in categories)
            
            print("\n📊 Горизонтальный график:")
            for cat in categories:
                bar_length = int(40 * cat['ads_count'] / max_count) if max_count > 0 else 0
                bar = '█' * bar_length
                print(f"{cat['name'][:15]:15} | {bar} {cat['ads_count']}")
    
    def export_to_csv(self):
        """Экспорт объявлений в CSV файл"""
        print("\n" + "=" * 60)
        print("ЭКСПОРТ В CSV")
        print("=" * 60)
        
        import csv
        
        filename = f"ads_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        with self.conn.cursor(cursor_factory=extras.RealDictCursor) as cur:
            cur.execute("""
                SELECT 
                    a.id,
                    a.title,
                    a.price,
                    c.name as category,
                    a.city,
                    a.seller,
                    a.views,
                    a.is_active,
                    a.created_at
                FROM ads a
                JOIN categories c ON a.category_id = c.id
                ORDER BY a.created_at DESC
            """)
            
            ads_data = cur.fetchall()
            
            if not ads_data:
                print("Нет данных для экспорта")
                return
            
            # Записываем в CSV
            with open(filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
                if ads_data:
                    fieldnames = ads_data[0].keys()
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(ads_data)
            
            print(f"✅ Экспортировано {len(ads_data)} объявлений")
            print(f"📁 Файл сохранён как: {filename}")
            
            # Покажем первые несколько строк
            print("\n👀 Первые 3 записи:")
            with open(filename, 'r', encoding='utf-8-sig') as csvfile:
                for i, line in enumerate(csvfile):
                    if i > 3:
                        break
                    print(line.strip())
    
    def show_activity_heatmap(self):
        """Тепловая карта активности по дням недели и часам"""
        print("\n" + "=" * 60)
        print("ТЕПЛОВАЯ КАРТА АКТИВНОСТИ")
        print("=" * 60)
        
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT 
                    EXTRACT(DOW FROM created_at) as day_of_week,
                    EXTRACT(HOUR FROM created_at) as hour,
                    COUNT(*) as ads_count
                FROM ads
                GROUP BY day_of_week, hour
                ORDER BY day_of_week, hour
            """)
            
            data = cur.fetchall()
            
            if not data:
                print("Нет данных")
                return
            
            # Создаём матрицу 7x24
            matrix = [[0 for _ in range(24)] for _ in range(7)]
            max_count = 0
            
            for day, hour, count in data:
                day = int(day)
                hour = int(hour)
                if 0 <= day <= 6 and 0 <= hour <= 23:
                    matrix[day][hour] = count
                    if count > max_count:
                        max_count = count
            
            # Дни недели
            days = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']
            
            print("\n📊 Активность по часам (0-23) и дням недели:")
            print("    " + " ".join([f"{h:2}" for h in range(24)]))
            
            for day_idx, day_name in enumerate(days):
                row = f"{day_name}: "
                for hour in range(24):
                    count = matrix[day_idx][hour]
                    if count == 0:
                        row += " ·"
                    elif count < max_count * 0.3:
                        row += " ░"
                    elif count < max_count * 0.7:
                        row += " ▒"
                    else:
                        row += " █"
                print(row)

    def run(self):
        """Запуск главного меню"""
        print("=" * 60)
        print("🏠 МЕНЕДЖЕР ОБЪЯВЛЕНИЙ (PostgreSQL версия)")
        print("=" * 60)
        print("Добро пожаловать!")
        
        try:
            while True:
                print("\n" + "-" * 40)
                print("ГЛАВНОЕ МЕНЮ:")
                print("  1. Показать все объявления")
                print("  2. Добавить объявление")
                print("  3. Поиск объявлений")
                print("  4. Топ объявлений")
                print("  5. Редактировать объявление")
                print("  6. Удалить объявление")
                print("  --- Статистика и аналитика ---")
                print("  7. Общая статистика")
                print("  8. Статистика по времени")
                print("  9. График по категориям")
                print(" 10. Тепловая карта активности")
                print("  --- Экспорт ---")
                print(" 11. Экспорт в CSV")
                print("  0. Выход")
                print("-" * 40)
                
                choice = input("Выберите действие: ").strip()
                
                if choice == "1":
                    self.show_all_ads()
                elif choice == "2":
                    self.add_new_ad()
                elif choice == "3":
                    self.search_ads()
                elif choice == "4":
                    self.show_top_ads()
                elif choice == "5":
                    self.update_ad()
                elif choice == "6":
                    self.delete_ad()
                elif choice == "7":
                    self.show_statistics()
                elif choice == "8":
                    self.show_time_stats()
                elif choice == "9":
                    self.show_category_chart()
                elif choice == "10":
                    self.show_activity_heatmap()
                elif choice == "11":
                    self.export_to_csv()
                elif choice == "0":
                    print("\nДо свидания!")
                    break
                else:
                    print("Неверный выбор")
                
                input("\nНажмите Enter, чтобы продолжить...")
        
        finally:
            self.close()
# ============================================================
# ЗАПУСК
# ============================================================
if __name__ == "__main__":
    manager = AdManager()
    manager.run()
