# ![example workflow](https://github.com/IlyaYaP/foodgram-project-react/actions/workflows/main.yml/badge.svg)

# Проект Foodgram
Foodgram - продуктовый помощник с базой кулинарных рецептов. Пользователям предоставлена возможность просмотра опубликованных рецептов и публикации собственных. Доступна возможность подписки на авторов, добавление рецептов в избранное,  а так же скачивание списка покупок.
  
### Стек технологий:
Стек: Python 3.7, Django, DRF, PostgreSQL, Docker, nginx, gunicorn.



# Развертывание проекта на удаленном сервере
Склонируйте репозиторий. 
```
https://github.com/IlyaYaP/foodgram-project-react.git
```
Создайте .env файл в директории infra/, в котором должны содержаться следующие переменные для подключения к базе PostgreSQL:
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```
Скопировать на сервер файлы docker-compose.yml, nginx.conf из папки infra (команды выполнять находясь в папке infra):
```
scp docker-compose.yml nginx.conf username@IP:/home/username/
```
Создать и запустить контейнеры Docker, выполнить команду на сервере:
```
sudo docker compose up -d
```
После успешной сборки выполнить миграции, собрать статику, наполнить базу, создать суперпользователя:
```
sudo docker compose exec backend python manage.py migrate
sudo docker compose exec backend python manage.py collectstatic --noinput
sudo docker compose exec backend python manage.py load_ingredients
sudo docker compose exec backend python manage.py createsuperuser
```
```
Сервер развернут на виртуальной машине:
```
https://console.cloud.yandex.ru
```
Публичный IP:
```
84.201.175.127
```
### Разработчики проекта(backend):

 - Козырев Илья 
