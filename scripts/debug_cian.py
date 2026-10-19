from playwright.sync_api import sync_playwright
from pathlib import Path
import time

# URL для долгосрочной аренды квартир в Москве (как в вашем основном скрипте)
URL = "https://www.cian.ru/cat.php?deal_type=rent&engine_version=2&offer_type=flat&region=1&type=4"

# Папка для сохранения отладочного HTML
DEBUG_DIR = Path("data/raw/html")
DEBUG_DIR.mkdir(parents=True, exist_ok=True)

with sync_playwright() as p:
    print("Запускаем браузер Chromium...")
    browser = p.chromium.launch(headless=False)  # headless=False — вы увидите окно браузера
    page = browser.new_page()
    
    print(f"Переходим на {URL}...")
    page.goto(URL, timeout=60000)
    
    # Ждём загрузки (можно увеличить, если сайт медленный)
    print("Ждём 10 секунд, чтобы страница точно загрузилась...")
    time.sleep(10)
    
    # Сохраняем HTML
    html_content = page.content()
    debug_file = DEBUG_DIR / "cian_debug_page.html"
    debug_file.write_text(html_content, encoding="utf-8")
    print(f"HTML сохранён в: {debug_file.resolve()}")
    
    # Проверяем размер
    print(f"Размер HTML: {len(html_content)} символов")
    
    # Ищем признаки объявлений или капчи
    if "captcha" in html_content.lower() or "подтвердите, что вы не робот" in html_content.lower():
        print("⚠️ В HTML найдены признаки капчи или проверки на бота.")
    elif "OfferTitle" in html_content or "data-name=\"Offers\"" in html_content:
        print("✅ В HTML найдены признаки структуры с объявлениями (OfferTitle / Offers).")
    else:
        print("❓ Не удалось однозначно определить содержимое. Откройте сохранённый файл.")
    
    browser.close()

print("Готово. Откройте сохранённый HTML-файл в браузере или текстовом редакторе и посмотрите, есть ли там карточки квартир.")