В папке apiwork лежит Dockerfile, его нужно запустить из директории командой
'docker build -t test-django-docker .'. После флага -t можете написать любое имя образа.
Далее перемещаетесь в директорию выше, в которой лежит файл docker-compose.yml.
Выполните команду 'docker-compose up' для запуска контейнеров с джанго-сервером, postgres, nginx.
При сборке контейнера superuser уже будет создан (admin:admin).
API проверены на локальной машине с помощью Postman.