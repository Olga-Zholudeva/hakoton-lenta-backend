# Предсказательная модель для компании "Лента"

## Суть проекта:

Данный проект дает возможность сотрудниками компании "Лента" ежедневно получать прогноз на 14 дней вперед. Прогноз осуществляется по скю, которые относятся к собственному производству и имеют короткой срок реализации. 

У пользователей ресурса есть возможность фильтрации данных по:

- Городу/ам
- Магазину/ам
- Группе/ам товаров
- Категории/ям
- Подкатегории/ям
- Товару/ам
- Сгруппировать данные по дню/неделе/месяцу

Также у пользователей есть возможность выгрузить данные в excel.

## Технологии проекта:

- Django 4.2.5
- DRF 3.14.0
- Djoser 2.1.0
- drf-yasg 1.21.7
- openpyxl 3.1.2

## Локальный запуск в Docker:

- Клонируем репозиторий: **git clone [Предсказательная модель для компании "Лента"](https://github.com/K1N88/hakoton-lenta-backend.git)**
- Создаем и заполняем файл .env по образцу из **.env.example**
- В директории infra_local запускаем сборку контейнеров БД PostgreSQL, backend, ML и nginx: **docker compose up -d**
- Выполняем миграции: **docker compose exec backend python manage.py migrate**
- Собираем статические файлы и медиа: **docker compose exec backend python manage.py collectstatic**
- Создаем пользователя с правами суперюзера: **docker compose exec backend python manage.py createsuperuser**

После запуска проекта документация swagger будет доступна тут: **http://localhost/swagger/**

## Загрузка тестовых данных:

- Даные по магазинам: **docker compose exec backend python manage.py st_df**
- Даные по товарам: **docker compose exec backend python manage.py pr_df**
- Фактические данные по продажам: **docker compose exec backend python manage.py sales_df**
- Прогноз: **docker compose exec backend python manage.py forecast_df**

## Проект выполнили:

- Константин Назаров
- Ольга Жолудева