import logging
logging.basicConfig(level=logging.DEBUG)
from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2
from psycopg2 import extras
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Для flash-сообщений

# Параметры подключения к БД
DB_PARAMS = {
    "dbname": "avito_clone",
    "user": os.getenv("USER"),  # ваше имя пользователя
    "host": "localhost"
}

def get_db_connection():
    """Получить соединение с базой данных"""
    return psycopg2.connect(**DB_PARAMS)

@app.route('/')
def index():
    """Главная страница"""
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)
    
    # Получаем статистику
    cur.execute("SELECT COUNT(*) as total FROM ads")
    total_ads = cur.fetchone()['total']
    
    cur.execute("SELECT COUNT(*) as active FROM ads WHERE is_active = true")
    active_ads = cur.fetchone()['active']
    
    cur.execute("SELECT COUNT(*) as total FROM categories")
    total_categories = cur.fetchone()['total']
    
    cur.close()
    conn.close()
    
    return render_template('index.html', 
                         total_ads=total_ads,
                         active_ads=active_ads,
                         total_categories=total_categories)

@app.route('/ads')
def list_ads():
    """Список всех объявлений"""
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)
    
    cur.execute("""
        SELECT a.*, c.name as category_name 
        FROM ads a
        JOIN categories c ON a.category_id = c.id
        WHERE a.is_active = true
        ORDER BY a.created_at DESC
    """)
    
    ads = cur.fetchall()
    cur.close()
    conn.close()
    
    # ВАЖНО: здесь ДОЛЖЕН БЫТЬ ads.html, НЕ add_ad.html
    return render_template('ads.html', ads=ads)    

@app.route('/add', methods=['GET', 'POST'])
def add_ad():
    """Добавление нового объявления"""
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)
    
    # Получаем список категорий для выпадающего списка
    try:
        cur.execute("SELECT id, name FROM categories ORDER BY name")
        categories = cur.fetchall()
        print(f"Загружено категорий: {len(categories)}")  # Отладка
    except Exception as e:
        print(f"Ошибка загрузки категорий: {e}")
        categories = []
    
    if request.method == 'POST':
        # Получаем данные из формы
        title = request.form.get('title', '').strip()
        price = request.form.get('price', '').strip()
        category_id = request.form.get('category_id', '').strip()
        city = request.form.get('city', '').strip()
        seller = request.form.get('seller', '').strip()
        
        print(f"Получены данные: title={title}, price={price}, category_id={category_id}")  # Отладка
        
        # Проверка обязательных полей
        if not all([title, price, category_id, city, seller]):
            flash('❌ Все поля обязательны для заполнения!', 'error')
            cur.close()
            conn.close()
            return render_template('add_ad.html', categories=categories)
        
        try:
            # Вставляем новое объявление
            cur.execute("""
                INSERT INTO ads (title, price, category_id, city, seller, views)
                VALUES (%s, %s, %s, %s, %s, 0)
                RETURNING id
            """, (title, int(price), int(category_id), city, seller))
            
            new_id = cur.fetchone()['id']
            conn.commit()
            print(f"✅ Добавлено объявление с ID: {new_id}")  # Отладка
            
            flash('✅ Объявление успешно добавлено!', 'success')
            cur.close()
            conn.close()
            return redirect(url_for('list_ads'))
            
        except Exception as e:
            conn.rollback()
            print(f"❌ Ошибка при добавлении: {e}")  # Отладка
            flash(f'❌ Ошибка: {e}', 'error')
    
    cur.close()
    conn.close()
    return render_template('add_ad.html', categories=categories)
@app.route('/ad/<int:ad_id>')
def view_ad(ad_id):
    """Просмотр конкретного объявления"""
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)
    
    # Увеличиваем счётчик просмотров
    cur.execute("UPDATE ads SET views = views + 1 WHERE id = %s", (ad_id,))
    conn.commit()
    
    cur.execute("""
        SELECT a.*, c.name as category_name 
        FROM ads a
        JOIN categories c ON a.category_id = c.id
        WHERE a.id = %s
    """, (ad_id,))
    
    ad = cur.fetchone()
    cur.close()
    conn.close()
    
    if not ad:
        flash('❌ Объявление не найдено', 'error')
        return redirect(url_for('list_ads'))
    
    return render_template('view_ad.html', ad=ad)

@app.route('/delete/<int:ad_id>')
def delete_ad(ad_id):
    """Удаление (деактивация) объявления"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("UPDATE ads SET is_active = false WHERE id = %s", (ad_id,))
    conn.commit()
    
    cur.close()
    conn.close()
    
    flash('✅ Объявление деактивировано', 'success')
    return redirect(url_for('list_ads'))

@app.route('/stats')
def statistics():
    """Статистика"""
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)
    
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
    
    # Статистика по категориям
    cur.execute("""
        SELECT 
            c.name,
            COUNT(a.id) as ads_count,
            SUM(a.views) as total_views,
            AVG(a.price) as avg_price
        FROM categories c
        LEFT JOIN ads a ON c.id = a.category_id AND a.is_active = true
        GROUP BY c.name
        HAVING COUNT(a.id) > 0
        ORDER BY ads_count DESC
    """)
    category_stats = cur.fetchall()
    
    cur.close()
    conn.close()
    
    return render_template('stats.html', stats=stats, category_stats=category_stats)

@app.route('/about')
def about():
    """Страница о проекте"""
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)



