![Workflow Result](https://github.com/grmzk/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

# YaMDb (docker-container)
Docker-контейнер для развертывания бэкенд API проекта YaMDb (ресурс для публикации отзывов к произведениям 
искусства и формирования их рейтинга)

##### Технологии
- Python 3
- Django 3.2
- Django REST Framework 3.12
- Docker
- PostgreSQL 13.0
- Nginx 1.21.3
##### Как запустить проект:

Клонировать репозиторий и перейти в директорию `infra` в командной строке:

```
git clone git@github.com:grmzk/infra_sp2.git
```

```
cd infra_sp2/infra/
```

Для работы с другой СУБД отредактировать `.env`

```
DB_ENGINE=django.db.backends.postgresql # СУБД 
DB_NAME=postgres                        # название БД
POSTGRES_USER=postgres                  # имя пользователя БД
POSTGRES_PASSWORD=postgres              # пароль пользователя БД
DB_HOST=db                              # адрес хоста с БД
DB_PORT=5432                            # порт для подключения к БД
```

Собрать контейнер и запустить YaMDb:

```
docker-compose up -d
```


Выполнить поочереди (только после первой сборки):

```
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic --no-input
```

##### Эндпоинты

Получить список всех произведений искусства:
```
GET /api/v1/titles/
```

Получить конкретную произведение по id:
```
GET /api/v1/titles/{id}/
```

Добавление отзыва к произведению:
```
JSON в теле запроса
{
    "text": "string",
    "score": "integer"
}

POST /api/v1/titles/{title_id}/reviews/
```

Полный список эндпоинтов:
```
http://62.84.120.127/redoc/
```

##### Авторы
- Игорь Музыка [mailto:igor@mail.fake]
- Денис Попченко [mailto:denis@mail.fake]
- Александр Романов [mailto:alex@mail.fake]
- Yandex LLC
Test