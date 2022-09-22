# Тестовое задание. Интеграция с платежной системой Stripe

Административная панель:
```sh
http://demonvr.ddns.net/admin/
```

Документация API:
```sh
http://demonvr.ddns.net/api/schema/swagger/
```

Получение stripe session_id для определенного товара:
```sh
http://demonvr.ddns.net/api/buy-item/{id}
```

Получение html страницы для определенного товара:
```sh
http://demonvr.ddns.net/api/item/{id}
```

## Номера тестовых кредитных карт

Номер карты для успешного платежа:

```sh
4242424242424242
```

Номер карты для отклонения платежа:

```sh
4000000000000002
```
остальные данные вводятся любые, но дата окончания карты должна быть не меньше текущей даты

## Запуск проекта:

```sh
docker-compose up -d --build
```

Применение миграций

```sh
docker-compose exec web python manage.py migrate
```

Создание администратора:

```sh
docker-compose exec web python manage.py createsuperuser
``` 