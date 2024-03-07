# Сайт с рецептами

Проект для сдачи второго модуля на онлайн курсе для Казанского Федерального Университета.

## Запуск проекта для разработки

- python -m venv venv - создание виртуального окружения
- `venv\Scripts\Activate.ps1` - вход в виртуальное окружение
- `pip install -r requirements.txt` - установка зависимостей
- установка [PostgreSQL](https://www.postgresql.org/)
- `python manage.py migrate` - применение миграций
- `python manage.py runserver` - запуск сервера для разработки на http://127.0.0.1:8000