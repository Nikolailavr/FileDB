# Тестовое задание: Написать файловую СУБД для работы с JSON/XML файлами

## Запуск контейнеров:

Перед запуском необходимо добавить IP адрес вашего сервера в ALLOWED_HOST в файле docker-compose.yml

```sh
$ docker-compose up -d --build
```

## HELP

### [POST] api/upload-file Загрузка файла с данными XML/JSON.

### [POST] api/upload-json Загрузка json с данными.

#### Тело запроса:

- type - Выбор между "type1" и "type2"
- vendor - строка на 50 символов
- date-revision  - Дата ревизии
- extra-field - Необязательные параметры (JSON)

### [POST] api/get Запрос данных из БД

### [GET] api/ping Проверка работы СУБД
