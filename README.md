# Анализ рынка аренды жилья в Москве

## 📋 Описание проекта
Исследование рынка долгосрочной аренды квартир в Москве для агентства недвижимости. Цель — выявить ключевые факторы, влияющие на цену, и дать рекомендации по формированию портфеля предложений.

## 🎯 Бизнес-проблема
Агентство недвижимости принимает решения о том, какие районы и типы квартир продвигать, интуитивно. Это ведёт к потере прибыли: в одних районах предложение избыточно, в других — дефицит. Нужен анализ данных, который подсветит перспективные сегменты.

## 📊 Данные
- **Источник:** Циан (cian.ru) — карточки объявлений долгосрочной аренды
- **Объём:** __ объявлений
- **Поля:** цена, площадь, количество комнат, этаж, тип дома, район, адрес
- **Способ сбора:** парсинг на Python (Requests + BeautifulSoup4)

## 🛠 Методология
1. **Сбор данных** — `scripts/scraper.py`
2. **Очистка и подготовка** — `notebooks/01_data_cleaning.ipynb`
3. **Загрузка в PostgreSQL** — `scripts/load_to_db.py`
4. **SQL-анализ** — `notebooks/02_sql_analysis.ipynb`
5. **Визуализация** — дашборд в Power BI (`powerbi/rental_market.pbix`)

## 🔍 Ключевые выводы
- _заполним после анализа_

## 💡 Рекомендации для бизнеса
- _заполним после анализа_

## 🧰 Стек технологий
Python (Requests, BeautifulSoup, Pandas), PostgreSQL, Power BI, DAX

## 📁 Структура проекта
```
├── data/
│ ├── raw/ # Сырые данные
│ └── processed/ # Очищенные данные
├── images/ # Скриншоты дашборда
├── notebooks/ # Jupyter ноутбуки
├── powerbi/ # Файлы Power BI
├── scripts/ # Python-скрипты
├── README.md
└── .gitignore
```

## 🚀 Как запустить
1. Клонируйте репозиторий.
2. Установите зависимости: `pip install -r requirements.txt`
3. Скопируйте `.env.example` → `.env` и впишите параметры БД.
4. Создайте БД `rental_market` в PostgreSQL.
5. Запустите `python scripts/scraper.py` — соберёт сырые данные.
6. Выполните `notebooks/01_data_cleaning.ipynb` — подготовит данные.
7. Запустите `python scripts/load_to_db.py` — загрузит в PostgreSQL.
8. Выполните `notebooks/02_sql_analysis.ipynb` — SQL-запросы.
9. Откройте `powerbi/rental_market.pbix` — дашборд.

## 👤 Автор
Сухих Вета, начинающий аналитик данных
- GitHub: [@veta-suhih](https://github.com/veta-suhih)
- LinkedIn: [@vetasuhih](https://www.linkedin.com/in/vetasuhih)
- Telegram: [@veta_suhih](https://t.me/veta_suhih)
- Email: [veta.suhih@gmail.com](mailto:veta.suhih@gmail.com)