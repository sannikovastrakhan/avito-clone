import psycopg2
from psycopg2 import sql

# Параметры подключения
conn_params = {
    "dbname": "avito_clone",
    "user": "sergejsannikov",  # ваше имя пользователя (обычно совпадает с именем в системе)
    "host": "localhost"
}

try:
    # Подключаемся к базе
    conn = psycopg2.connect(**conn_params)
    cur = conn.cursor()
    
    print("✅ Подключение к базе данных успешно!")
    
    # Простой запрос
    cur.execute("SELECT COUNT(*) FROM ads")
    count = cur.fetchone()[0]
    print(f"📊 В базе {count} объявлений")
    
    # Выведем все объявления
    print("\n📋 Список объявлений:")
    cur.execute("""
        SELECT ads.title, ads.price, categories.name 
        FROM ads 
        JOIN categories ON ads.category_id = categories.id
        LIMIT 5
    """)
    
    for row in cur.fetchall():
        print(f"  • {row[0]} — {row[1]} ₽ ({row[2]})")
    
    cur.close()
    conn.close()
    
except Exception as e:
    print(f"❌ Ошибка: {e}")
