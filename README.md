# Проектная работа 8 спринта

Проектные работы в этом модуле выполняются в командах по 3 человека. Процесс обучения аналогичен сервису, где вы изучали асинхронное программирование. Роли в команде и отправка работы на ревью не меняются.

Распределение по командам подготовит команда сопровождения. Куратор поделится с вами списками в Slack в канале #group_projects.

Задания на спринт вы найдёте внутри тем.


Примеры запроса для ugc_api:

- добавление отсмотренного временного фрейма:

http://127.0.0.1/api/v1/view_progress

```json
{
    "user_id": "39611654-27bb-49af-bf31-a931cd3b0e7f",
    "type": "view_progress",
    "movie_id": "88322538-e1a1-4a36-9154-f62e62579723",
    "movie_timestamp": 361112
}
```
- поставить лайк фильму:

http://127.0.0.1/api/v1/likes

```json
{
    "user_id": "39611654-27bb-49af-bf31-a931cd3b0e7f",
    "movie_id": "88322538-e1a1-4a36-9154-f62e62579723"
}
```

- положить фильм в закладки:

http://127.0.0.1/api/v1/bookmarks

```json
{
    "user_id": "39611654-27bb-49af-bf31-a931cd3b0e7f",
    "movie_id": "88322538-e1a1-4a36-9154-f62e62579723"
}
```
- добавить рецензию к фильму:

http://127.0.0.1/api/v1/reviews

```json
{
    "user_id": "39611654-27bb-49af-bf31-a931cd3b0e7f",
    "movie_id": "88322538-e1a1-4a36-9154-f62e62579723",
    "text": "this movie is a masterpiece!"
}
```

## Тестирование
- Запустить `make test`
- Результат теста смотреть в контейнере `tests`

## Ссылка на репозиторий

https://github.com/bogatovad/ugc_sprint_1


### Выбор реализации сервиса

Сервис для сохранения пользовательских лайков, закладок, рецензий и другого UC было решено вынести в отдельный сервис (ugc_2), т.к:
- ugc_2 использует в качестве хранилищ MongoDB, куда пользовательский контент сохраняется напрямую. 
А сервис ugc использует Kafka для стримминга событий просмотра фильмов и ClickHouse в качестве OLAP хранилища.
Таким образом каждый микросервис использует свое отдельное хранилище, что повышает отказоустойчивость каждого компонента и системы в целом, а так же дает возможности для гибкого горизонтального масштабирования каждого из компонентов, т.к.каждый сервис масштабируется назависимо. 

- разделение бизнес-логики: разделение на отдельные микросервисы упрощает реализацию и поддержку всего сервиса UGC, функционал которого  может разрастаться. ugc, по сути, предоставляет API для стримминга событий в Kafka, а ugc_2 - взаимодействие с MongoDB. Разделение ответственности и бизнес-логики между этими микросервисами позволяет не только заменять хранилища при необходимости, но и полностью заменить отдельно взятый микросервис (например, использовать другой фреймворк или даже другой язык программирования), без каких внесения каких либо измений в код другого микросервиса.

Минусы такого подхода:

- Усложняется развертывание и поддержка инфраструктуры проекта.

- Данные, необходимые для работы сервиса или аналитиков, находятся в разных хранилищах, приходиться их агрегировать через дополнительные прослойки. 

