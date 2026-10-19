"""
scripts/scraper.py

Собирает объявления о долгосрочной аренде квартир в Москве с Циан (cian.ru).

Подход: библиотека cianparser (форк с поддержкой заголовков браузера), которая
управляет реальным Chromium через Playwright. Сбор разбит на пакеты страниц
с паузами между вызовами, чтобы не провоцировать блокировку по IP.

Запуск (из корня проекта, с активированным venv):
    python scripts/scraper.py
"""

import time
from pathlib import Path

import pandas as pd
import cianparser


# ── Конфигурация ─────────────────────────────────────────────────────────────
LOCATION = "Москва"
DEAL_TYPE = "rent_long"     # долгосрочная аренда
ROOMS = "all"               # все комнатности

# 🎯 ЦЕЛЕВОЙ ОБЪЁМ ДАННЫХ
# Одна страница ~28 объявлений.
# 1000 объявлений ≈ 36 страниц. 5000 объявлений ≈ 180 страниц.
TARGET_END_PAGE = 180        # Установите 36 для ~1000, 180 для ~5000

# 📦 РАЗМЕР ПАКЕТА: сколько страниц собираем за один вызов get_flats
PAGES_PER_BATCH = 5

# ⏱️ ПАУЗА МЕЖДУ ПАКЕТАМИ (в секундах). Даём сайту "остыть".
PAUSE_BETWEEN_BATCHES = 20


PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_ROOT / "data" / "raw"
OUTPUT_CSV = RAW_DIR / "rent_offers_raw.csv"


def main() -> None:
    print("=" * 60)
    print("Парсинг рынка аренды квартир в Москве (Циан)")
    print(f"Целевой диапазон страниц: 1–{TARGET_END_PAGE}")
    print(f"Размер пакета: {PAGES_PER_BATCH} страниц, пауза между пакетами: {PAUSE_BETWEEN_BATCHES} сек.")
    print("=" * 60)

    RAW_DIR.mkdir(parents=True, exist_ok=True)

    all_offers = []
    current_start = 1

    while current_start <= TARGET_END_PAGE:
        current_end = min(current_start + PAGES_PER_BATCH - 1, TARGET_END_PAGE)

        print(f"\n→ Пакет страниц {current_start}–{current_end}...")

        parser = cianparser.CianParser(location=LOCATION)
        try:
            batch_data = parser.get_flats(
                deal_type=DEAL_TYPE,
                rooms=ROOMS,
                with_saving_csv=False,
                additional_settings={
                    "start_page": current_start,
                    "end_page": current_end,
                },
            )
        except Exception as exc:
            print(f"  ❌ Ошибка при сборе пакета: {exc}")
            print("  Пропускаем пакет и продолжаем...")
            batch_data = []

        if batch_data:
            all_offers.extend(batch_data)
            print(f"  ✅ Собрано в пакете: {len(batch_data)}. Всего: {len(all_offers)}")
        else:
            print("  ⚠️ Пакет пуст.")

        # Пауза перед следующим пакетом, если это не последний
        if current_end < TARGET_END_PAGE:
            print(f"  ⏳ Пауза {PAUSE_BETWEEN_BATCHES} секунд перед следующим пакетом...")
            time.sleep(PAUSE_BETWEEN_BATCHES)

        current_start = current_end + 1

    if not all_offers:
        print("\n❌ Ни одного объявления не собрано. Проверьте настройки и подключение.")
        return

    df = pd.DataFrame(all_offers)
    before = len(df)

    if "url" in df.columns:
        df = df.drop_duplicates(subset=["url"]).reset_index(drop=True)
    else:
        df = df.drop_duplicates().reset_index(drop=True)

    df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")

    print("\n" + "=" * 60)
    print(f"✅ Готово. Собрано объявлений: {len(df)} (дублей удалено: {before - len(df)})")
    print(f"   Файл: {OUTPUT_CSV.relative_to(PROJECT_ROOT)}")
    print("=" * 60)


if __name__ == "__main__":
    main()