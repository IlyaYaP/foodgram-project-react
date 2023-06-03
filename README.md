# ![example workflow](https://github.com/IlyaYaP/foodgram-project-react/actions/workflows/main.yml/badge.svg)

# Проект Foodgram
Foodgram - продуктовый помощник с базой кулинарных рецептов. Пользователям предоставлена возможность просмотра опубликованных рецептов и публикации собственных. Доступна возможность подписки на авторов, добавление рецептов в избранное,  а так же скачивание списка покупок.
  
### Стек технологий:
Стек: Python 3.7, Django, DRF, PostgreSQL, Docker, nginx, gunicorn.

# Развертывание проекта локально
-  Клонируем репозиторий с проектом:
```
git clone https://github.com/IlyaYaP/foodgram-project-react.git
```
-  В папке с проектом создаем и активируем виртуальное окружение:
```
python -m venv venv
source venv/scripts/activate
```
-  Устанавливаем зависимости:
```
cd backend/foodgram
python -m pip install --upgrade pip
pip install -r requirements.txt
```
-  Создаем .env файл в директории infra/, в котором должны содержаться следующие переменные для подключения к базе PostgreSQL:
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```
-  Создаем и запускаем контейнеры Docker:
```
docker-compose up -d
```

-  После успешного запуска контейнеров выполним миграции, соберем статику, наполним бд и создаим суперюзера:
```
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py collectstatic --noinput
docker-compose exec backend python manage.py load_ingredients
docker-compose exec backend python manage.py createsuperuser
```
Проект доступен по адресу:
```
http://localhost/
```

# Развертывание проекта на удаленном сервере
 - Склонируйте репозиторий. 
```
https://github.com/IlyaYaP/foodgram-project-react.git
```
 - Создайте .env файл в директории infra/, в котором должны содержаться следующие переменные для подключения к базе PostgreSQL:
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```
 - Скопировать на сервер файлы docker-compose.yml, nginx.conf из папки infra (команды выполнять находясь в папке infra):
```
scp docker-compose.yml nginx.conf username@IP:/home/username/
```
 - Создать и запустить контейнеры Docker, выполнить команду на сервере:
```
sudo docker compose up -d
```
 - После успешной сборки выполнить миграции, собрать статику, наполнить базу, создать суперпользователя:
```
sudo docker compose exec backend python manage.py migrate
sudo docker compose exec backend python manage.py collectstatic --noinput
sudo docker compose exec backend python manage.py load_ingredients
sudo docker compose exec backend python manage.py createsuperuser
```

Сервер развернут на виртуальной машине:
```
https://console.cloud.yandex.ru
```
Проект доступен по адресу:
```
http://51.250.81.74/
```
Данные суперпользователя:
```
email: admin@ya.ru
password: admin
```
### Разработчики проекта(backend):

 - Козырев Илья 
