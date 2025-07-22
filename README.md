# Weather Query API

Простое веб-приложение на FastAPI, позволяющее получать текущие данные о погоде по названию города, сохранять запросы и отображать историю.

---

## Описание

Приложение:

- Принимает название города через POST-запрос `/weather/`
- Запрашивает данные о погоде у публичного API (например, OpenWeatherMap)
- Сохраняет данные запроса в базу PostgreSQL
- Позволяет получить список всех предыдущих запросов через GET `/history/`

---

## Технологии

- Python 3.10+
- FastAPI
- Async SQLAlchemy
- PostgreSQL
- Docker (приложение + база)

---

## Установка и запуск

1. Клонируйте репозиторий:

```bash
git clone <https://github.com/Anton-Burdey/weather-query-app>
cd <weather-query-app>
