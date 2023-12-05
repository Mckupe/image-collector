# image-collector

Чтобы получить изображения: http://127.0.0.1:8000/get_images/{enum линии}
Названия линии в файле config.py
Создание образа
docker image build -t image-collector-0.1:latest -f Dockerfile .
Запуск и создание контейнера 
docker run -d --name image-collector -p 80:80 image-collector-0.1
Пройти в всаггер:
http://127.0.0.1/docs