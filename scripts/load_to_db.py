"""
scripts/load_to_db.py

Загружает очищенный датасет rent_offers_clean.csv в PostgreSQL
в таблицу rent_offers. Создаёт индексы для ускорения аналитических запросов.

Запуск (из корня проекта, с активированным venv):
    python scripts/load_to_db.py
"""

import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text


# Загружаем переменные из .env (в корне проекта)
PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

PROCESSED_CSV = PROJECT_ROOT / "data" / "processed" / "rent_offers_clean.csv"

DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "rental_market")


def main() -> None:
    if not DB_PASSWORD:
        raise SystemExit("❌ В .env не задан DB_PASSWORD. Проверьте файл .env.")

    print("=" * 60)
    print(f"Загрузка данных в PostgreSQL: {DB_HOST}:{DB_PORT}/{DB_NAME}")
    print("=" * 60)

    # 1. Читаем очищенный CSV
    print(f"\n1. Читаем {PROCESSED_CSV.relative_to(PROJECT_ROOT)}...")
    df = pd.read_csv(PROCESSED_CSV)
    print(f"   Строк: {len(df)}, колонок: {len(df.columns)}")

    # 2. Подключаемся к БД
    url = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    engine = create_engine(url)

    # 3. Загружаем таблицу (перезаписываем, если существует — удобно при итерациях)
    print(f"\n2. Загружаем таблицу rent_offers (replace)...")
    df.to_sql("rent_offers", engine, if_exists="replace", index=False)

    # 4. Индексы для типичных GROUP BY / фильтров в аналитических запросах
    print("\n3. Создаём индексы...")
    with engine.begin() as conn:
        conn.execute(text(
            "CREATE INDEX IF NOT EXISTS idx_rent_offers_district "
            "ON rent_offers(district)"
        ))
        conn.execute(text(
            "CREATE INDEX IF NOT EXISTS idx_rent_offers_rooms "
            "ON rent_offers(rooms)"
        ))
        conn.execute(text(
            "CREATE INDEX IF NOT EXISTS idx_rent_offers_author_type "
            "ON rent_offers(author_type)"
        ))
        # Обновляем статистику планировщика — запросы будут быстрее
        conn.execute(text("ANALYZE rent_offers"))

    # 5. Проверяем, что данные на месте
    with engine.connect() as conn:
        row_count = conn.execute(text("SELECT COUNT(*) FROM rent_offers")).scalar()
        print(f"\n4. Проверка — строк в таблице: {row_count}")

        sample = conn.execute(text(
            "SELECT district, rooms, price, price_per_sqm "
            "FROM rent_offers WHERE district IS NOT NULL "
            "ORDER BY price DESC LIMIT 3"
        )).fetchall()
        print("\n   Топ-3 самых дорогих объявления в базе:")
        for row in sample:
            print(f"     {row[0]:20s} | {row[1]} комн. | {row[2]:>10,} ₽ | {row[3]:>6} ₽/м²")

    print("\n" + "=" * 60)
    print("✅ Готово. Данные в PostgreSQL, можно писать SQL-анализ.")
    print("=" * 60)


if __name__ == "__main__":
    main()