# Интеграция с платежной системой Stripe

Административная панель:

https://demonvr.sytes.net/admin/

Документация API:

https://demonvr.sytes.net/api/schema/swagger/


Получение stripe session_id для определенного товара:

https://demonvr.sytes.net/api/buy-item/{id}


Получение html страницы для определенного товара:

https://demonvr.sytes.net/api/item/{id}


## Номера тестовых кредитных карт

Номер карты для успешного платежа:

```sh
4242424242424242
```

Номер карты для неудачного платежа:

```sh
4000000000009995
```
> Остальные данные вводятся любые, но дата окончания карты должна быть не меньше текущей даты

## Запуск проекта (для разработки):

```sh
docker compose --env-file .env -f docker-compose.dev.yml up -d --build 
```

Применение миграций

```sh
docker-compose exec web python manage.py migrate
```

Создание администратора:

```sh
docker-compose exec web python manage.py createsuperuser
``` 

## Запуск проекта (для продакшена):

Build web image:

```sh
docker buildx build --platform=linux/amd64 -t  payment-forms-proxy-prod:amd64 . -f Dockerfile.prod    
```

Save web image:

```sh
docker save <image_id> | gzip > backup/docker/payment-forms-web-prod.tar.gz
```

Перенести образ на vps/vds, загрузить, создать тэг

```sh
docker load < payment-forms-web-prod.tar.gz # загрузить образ
docker tag <image_id> payment-forms-web-prod:amd64 # создать тэг
```

Поднять контейнеры:

```sh
docker compose --env-file .env.prod -f docker-compose.prod.yml up -d --build
docker-compose exec web python manage.py migrate --noinput # применить миграции
docker-compose exec web python manage.py collectstatic --no-input --clear # собрать статические файлы
```

Контейнеры: 
- payment_forms_web 
- payment_forms_db
- proxy
- certbot

Создание задачи по таймеру на перевыпуск сертификата Lets Encrypt:
* скопировать из папки certbot файлы **certbot-renewal.service** и **certbot-renewal.timer** в /etc/systemd/system/
* зарегистрировать таймер:

```sh
systemctl start certbot-renewal.timer
systemctl enable --now certbot-renewal.timer
systemctl daemon-reload 
```
