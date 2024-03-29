# Запуск и проверка
В папке с проектом запустить `docker-compose up`. Для проверки результата запустить скрипт `requests.sh` который сделает
3 запроса. Каждый запрос должен вернуть `{message: success}`. Чтобы проверить запись данных в базу данных можно перейти
по адресу `localhost:8080` где запущен контейнер `adminer`. Данные для входа можно найти в `docker-compose.yml` или
`pipeline_service/.env`.

# Структура пайплайн сервиса
## Сервис
Перед стартом создаются таблицы в базе данных и тестовый пайплайн. Сервис состоит из одного эндпоинта, который принимает
изображение и id пайплайна. Из базы данных получаются данные о пайплайне, которые собираются в пайплайн. Через него
происходят манипуляции с изображением.

## Пайплайн
Исходя из задания сервис должен получать на вход только id пайплайна, а база данных хранит только его конфигурацию.
Следовательно, на стороне сервиса должна быть какая-то реализация. Сам пайплайн универсальный. Из данных он берет
шаги и очередность, которые записаны в виде строки в формате JSON. А также тип данных с которыми эти шаги работают.
Сами шаги описаны в виде классов реализующие один интерфейс. А тип данных как классы данных унаследованные от базового
класса с байтовым полем для изображения (т.к. все пайплайны будут работать с ними). Подобная структура позволяет
дописывать новые шаги для пайплайна, удалять из конфигурации старые или создавать новые для новых пайплайнов с новыми
классами данных, но при этом иметь ограничения для их правильной работы.

Реализован пайплайн со следующими шагами:
1. Обработка изображения.
2. Отправка изображения на сервер с моделью машинного обучения и получение результата.
3. Сохранение изображения и результата в базу.

## База данных
Созданы модели классов для пайплайна и для фиксации результатов обнаружения автомабиля на изображении. Также описаны
классы-репозитории через которые можно взаимодействовать с моделями базы данных.

# Сервис имитации модели машинного обучения.
Сервис состоит из одного эндпоинта. Он принимает изображение и отправляет ответ со случайными результатами в виде JSON
объекта с определенными ключами в случае обнаружение автомобиля, либо None если он не обнаружен.

# Нагрузка
Для ускорения работы сервиса все операции имеющие такую возможность написаны с применением асинхронных технологий.
Например, обращения к базе данных или запросы к другому сервису. Если сервис перестанет справляться с потоком запросов,
но физические ресурсы будут иметь запас, можно будет разбить сервис на несколько процессов стандартным способом добавив
воркеров (workers) при запуске uvicorn или guvicorn. Так же возможно настроить кеширование FastAPI. Для этого
понадобиться создать контейнер с Redis. Однако, концепция сервера заключается в том, что одинаковые данные у него
запрашиваться не будут, поэтому это не совсем целесообразно.