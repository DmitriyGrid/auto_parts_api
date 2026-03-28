# Auto Parts API

REST API для управления автозапчастями на стеке **FastAPI + PostgreSQL + SQLAlchemy + Alembic**.

---

## 📋 Требования

- Python 3.10+
- PostgreSQL 16+
- Docker (опционально)

---

## 🚀 Быстрый старт

### Вариант 1: Локальный запуск

1. Установите зависимости:
```bash
pip install -r requirements.txt
```

2. Настройте `.env`:
```env
DB_USER=postgres
DB_PASSWORD=postgres
DB_NAME=auto_parts_db
DB_HOST=localhost
DB_PORT=5433
APP_PORT=8000
```

3. Примените миграции:
```bash
alembic upgrade head
```

4. Запустите сервер:
```bash
python -m uvicorn app.main:app --port 8000
```

---

### Вариант 2: Docker

```bash
docker-compose up -d --build
```

API будет доступно на: http://localhost:4200

---

## 📖 Документация

После запуска откройте:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

---

## 🔧 API Endpoints

| Метод | Endpoint | Описание |
|-------|----------|----------|
| GET | `/api/v1/parts` | Получить список запчастей |
| POST | `/api/v1/parts` | Создать запчасть |
| GET | `/api/v1/parts/{id}` | Получить запчасть по ID |
| PUT | `/api/v1/parts/{id}` | Полное обновление |
| PATCH | `/api/v1/parts/{id}` | Частичное обновление |
| DELETE | `/api/v1/parts/{id}` | Удалить (Soft Delete) |

---

## 📁 Структура проекта

```
auto_parts_api/
├── app/
│   ├── controllers/      # Контроллеры (роутеры)
│   ├── models/           # SQLAlchemy модели
│   ├── schemas/          # Pydantic схемы
│   ├── services/         # Бизнес-логика
│   ├── config.py         # Конфигурация
│   ├── database.py       # Подключение к БД
│   └── main.py           # Точка входа
├── alembic/              # Миграции БД
├── .env                  # Переменные окружения
├── .env.example          # Пример .env
├── docker-compose.yml    # Docker конфигурация
├── requirements.txt      # Зависимости
└── README.md             # Этот файл
```

---

## 🧪 Тестирование

### Через Swagger UI
Откройте http://localhost:8000/docs и тестируйте через интерфейс.

### Через PowerShell
```powershell
# Получить все запчасти
curl http://localhost:8000/api/v1/parts

# Создать запчасть
curl -X POST http://localhost:8000/api/v1/parts `
  -H "Content-Type: application/json" `
  -d '{"name":"Тормозные колодки","part_number":"BRK-001","price":1500,"description":"Тест"}'
```

---

## 🐳 Docker

### Запуск
```bash
docker-compose up -d
```

### Остановка
```bash
docker-compose down
```

### Просмотр логов
```bash
docker-compose logs -f app
docker-compose logs -f postgres
```

---

## 📝 Особенности

- **Soft Delete** — записи не удаляются физически, а помечаются полем `deleted_at`
- **Пагинация** — поддержка `page` и `limit` параметров
- **Валидация** — Pydantic схемы для всех запросов
- **Миграции** — Alembic для управления схемой БД
- **Асинхронность** — asyncio + asyncpg

---

## 👤 Автор

Студент: Гридин Дмитрий
Группа: 090304-РПИб-023

---

## 📄 Лицензия

Учебный проект для лабораторной работы.
