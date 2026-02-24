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
                print("  3. Статистика")
                print("  0. Выход")
                print("-" * 40)
                
                choice = input("Выберите действие: ").strip()
                
                if choice == "1":
                    self.show_all_ads()
                elif choice == "2":
                    self.add_new_ad()
                elif choice == "3":
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
