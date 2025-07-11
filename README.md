# Superhero API - Django REST Framework
Django REST API для работы с данными о супергероях, интегрированное с Superhero API.

## 📌 Особенности:

🏗️ Чистая архитектура Django с разделением на приложения

🐳 Полная Docker-конфигурация для разработки и продакшена

🔍 Интеграция с внешним Superhero API

📊 Хранение данных в PostgreSQL

🔎 Гибкая система фильтрации героев

✅ Покрытие тестами ключевой функциональности


## 🛠 Технологический стек
- Backend: Django 3.2 + Django REST Framework
- База данных: PostgreSQL 13
- Контейнеризация: Docker + Docker-compose
- Тестирование: pytest + pytest-django


## 🚀 Быстрый старт

### Предварительные требования
- Docker 20.10+ 
- Docker-compose 1.29+

### Установка
1. Клонируйте репозиторий:
```
git clone https://github.com/yourusername/superhero-api.git
cd superhero-api
```

2. Создайте файл окружения:

```
cp .env.example .env
```
3. Заполните необходимые переменные в env.templates:

```ini
# Django
DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=True

# Database
DB_NAME=superhero_db
DB_USER=superhero_user
DB_PASSWORD=superhero_pass
DB_HOST=db
DB_PORT=5432

# Superhero API
SUPERHERO_API_TOKEN=your-access-token
```
4. Запустите проект:

```
docker-compose up --build
```

Приложение будет доступно по адресу: http://localhost:8000

## 🌐 API Endpoints
Базовый URL
http://localhost:8000/api/v1/

Создать нового героя
```text
POST /heroes/
Content-Type: application/json

{
    "name": "Batman"
}
```
Ответ:

```json
{
    "id": 1,
    "name": "Batman",
    "intelligence": 100,
    "strength": 26,
    "speed": 27,
    "power": 47
}
```
Получить список героев
```text
GET /heroes/list/
```
Параметры запроса (все необязательные):

- name - точное совпадение имени
- intelligence - числовое значение или gte:число/lte:число
- strength - числовое значение или gte:число/lte:число
- speed - числовое значение или gte:число/lte:число
- power - числовое значение или gte:число/lte:число

Примеры запросов:

```text
GET /heroes/list/?name=Batman
GET /heroes/list/?intelligence=gte:90
GET /heroes/list/?strength=lte:50&power=gte:80
```

## 🧪 Тестирование
Для запуска тестов выполните:

```bash
docker-compose exec web pytest
```
Активируйте виртуальное окружение:

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```
Установите зависимости для разработки:

```bash
pip install -r requirements.txt
```
Запустите миграции:

```bash
python manage.py migrate
```
Запустите сервер:

```bash
python manage.py runserver
```