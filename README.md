# image-collector

Чтобы получить изображения: http://127.0.0.1:8000/get_images/{enum линии}
Названия линии в файле config.py
Создание образа
docker image build -t poetry-test:latest -f Dockerfile .
Запуск и создание контейнера 
docker run -d --name poetrytest -p 80:80 poetry-test
Пройти в всаггер:
http://127.0.0.1/docs