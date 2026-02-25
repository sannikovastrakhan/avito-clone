#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Менеджер объявлений — версия с PostgreSQL
"""

import psycopg2
from psycopg2 import sql, extras

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
                print("  7. Статистика")
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
