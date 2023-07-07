# Foofgram

## Онлайн-сервис для публикации рецептов доступен по адресу: [nrthbnd.serveminecraft.net](https://nrthbnd.serveminecraft.net/)

### Автор:

- [Анастасия Боль](https://github.com/nrthbnd)

### Технологии:

- Python 3.9.10
- Django 4.2
- Django REST framework 3.14.0
- библиотека Simple JWT - работа с JWT-токеном
- JS (React)

На данном сервисе пользователи смогут делиться своими рецептами с другими пользователями, подписываться на публикации других пользователей, добавлять любимые рецепты в список "Избранное", а также скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд перед походом в магазин.

#### Документация к api проекта доступна после запуска сервера по адресу:

```
http://localhost:8000/redoc/
```

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:
```
git clone git@github.com:nrthbnd/foodgram-project-react.git
```

Cоздать и активировать виртуальное окружение:
```
python -m venv .venv
source venv/scripts/activate
```

Обновить pip
```
python -m pip install --upgrade pip
```

Создать миграции:
```
python manage.py makemigrations
```

Применить миграции:
```
python manage.py migrate
```

Запустить проект:
```
python manage.py runserver
```
