# Foodgram
![yamdb_workflow](https://github.com/kapkaevandrey/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)
## api_Foodgram
Пример запущенного сервиса:
[lucky-foodgram.tk](http://lucky-foodgram.tk/recipes)


### _Описание проекта_

> ***Гиппократ***  (_древнегреческий целитель, врач и философ_)
>>И те, что пишут не для славы, желают признания, что хорошо написали, а те, что читают их, — похвалы за то, что прочли.
-------------------------------------------------------------------

Проект API и готового фронтенда системы публикации кулинарных рецептов.
Проект создан для всех гурманов, любителей вкусной еды, любителей делится своими кулинарными навыками и для тех кто просто ищет интересный рецепт. Этот проект для всех и каждого, вы можете зарегистрировать на нём собрать свою собственную категорию избранных блюд или следить за публикациями понравившихся авторов.
Еда не только даёт нам энергию, но и может объединять людей.

### _Технологии_
 - _[Python 3.9.7](https://docs.python.org/3/)_
 - _[Django 3.2.10](https://docs.djangoproject.com/en/3.2/)_
 - _[Django REST framework 3.12.4](https://www.django-rest-framework.org/)_
 - _[Pillow 8.4.0](https://pillow.readthedocs.io/en/stable/)_
 - _[Djoser 2.1.0](https://djoser.readthedocs.io/en/latest/)_
 - _[Chardet 4.0.0](https://pypi.org/project/chardet/)_
 - _[Docker](https://www.docker.com/)_
 - _[Gunicorn 20.0.4](https://pypi.org/project/gunicorn/)_
 - _[Nginx 1.19.3](https://nginx.org/)_
### _Как запустить проект в контейнерах Docker_:

Клонировать репозиторий и перейти в него в командной строке:

```shell
git clone https://github.com/kapkaevandrey/foodgram-project-react.git
```

```shell
cd foodgram-project-react/infra
```

Запустите сборку и запуск контейнеров:

```shell
docker-compose up
```

Откройте другое окно терминала и выполните миграции:

```shell
docker-compose exec backend python manage.py makemigrations
docker-compose exec backend python manage.py migrate
```

Заполнить данные из дампа БД:

```shell
docker-compose exec backend python manage.py loaddata fixtures.json 
```

### Шаблон файла с переменными окружения **.env**
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432

SECRET_KEY=<Ваш уникальный криптографический ключ>
```

----------------------------------------------------------------
### Локализация
В проекте по умолчанию установлена русская локализация (ru) и все надписи переведены на русский язык. При необходимости вы можете обновить или создать записи и перевод сообщений используя следующую команду (выполняется из директории проекта или директории приложения):
```shell
~/project_dir> django-admin makemessages -l ru
```
Затем отредактируйте файл сообщения **.po** расположенный в папке locale каждого приложения следую инструкциям из официальной [документации](https://docs.djangoproject.com/en/3.2/topics/i18n/translation/#:~:text=the%20particular%20language.-,For,-example%2C%20if%20your.) 
После создания файла сообщения - и каждый раз, когда вы вносите в него изменения - вам нужно будет скомпилировать его в более эффективную форму для использования для этого используйте команду:
```shell
~/project_dir> django-admin compilemessages
```

☑️***Примечание:*** Если вы хотите загрузить данные в БД из набора фалов можете перейти по ссылке ниже

### [__Загрузка в базу данных с использованием JSON__](https://github.com/kapkaevandrey/foodgram-project-react/blob/master/Load%20Data.md)

-------------------------------------------------------------------
### _Пользовательские роли в проекте_:
1. **Аноним :alien:**
2. **Аутентифицированный пользователь :sunglasses:**
3. **Администратор :innocent:**

**Анонимные :alien:** пользователи могут:
1. Просматривать, список рецептов;
2. Просматривать отдельные рецепты;
3. Фильтровать рецепты по тегам.
4. Создавать аккаунт

**Аутентифицированные  (user)  :sunglasses:** пользователи могут:
1. Получать данные о **своей** учётной записи;
2. Изменять свой пароль;
3. Просматривать, публиковать, удалять и редактировать **свои** рецепты;
4. Добавлять понравившиеся рецепты в избранное и удалять из избранного;
5. Добавлять понравившиеся рецепты в список покупок и удалять из своего списка;
6. Подписываться на авторов и отписываться от них;
7. Скачать сводный файл с ингредиентами необходимыми для приготовления рецептов сохранённых в списке покупок;
***Примечание***: Доступ ко всем операциям записи, обновления и удаления доступны только после аутентификации и получения токена.


***Примечание***: 
Выбирайте администартора с умом.
> ***Бен Паркер*** 
>>С большой силой приходит большая ответственность.

**Администратор  (admin)  :innocent:** может:
1. Всё!!!
2. Реально абсолютно всё, он в этом проекте главный босс;
3. Получать информацию о пользователях;
4. Создавать пользователей, изменять их данные и удалять из проекта;
5. Так же может добавлять новые теги и виды ингредиентов;
6. Редактировать рецепты и блокировать пользователей.

### _Набор доступных эндпоинтов :point_down:_:
* `api/docs/redoc` - Подробная документация по работе API.
* `api/tags/` - Получение, списка тегов (_GET_).
* `api/ingredients/` - Получение, списка ингредиентов (_GET_).
* `api/ingredients/` - Получение ингредиента с соответствующим **id** (_GET_).
* `api/tags/{id}` - Получение, тега с соответствующим **id** (_GET_).
* `api/recipes/` - Получение списка с рецептами и публикация рецептов (_GET, POST_).
* `api/recipes/{id}` - Получение, изменение, удаление рецепта с соответствующим **id** (_GET, PUT, PATCH, DELETE_).
* `api/recipes/{id}/shopping_cart/` - Добавление рецепта с соответствующим **id** в список покупок и удаление из списка (_GET, DELETE_).
* `api/recipes/download_shopping_cart/` - Скачать файл со списком покупок TXT (в дальнейшем появиться поддержка PDF) (_GET_).
* `api/recipes/{id}/favorite/` - Добавление рецепта с соответствующим **id** в список избранного и его удаление (_GET, DELETE_).


* #### _Операции с пользователями :point_down:_:
  * `api/users/` - получение информации о пользователе и регистрация новых пользователей. (_GET, POST_). 
  * `api/users/{id}/` - Получение информации о пользователе. (_GET_).
  * `api/users/me/` - получение и изменение данных своей учётной записи. Доступна любым авторизованными пользователям (_GET_). 
  * `api/users/set_password/` - изменение собственного пароля (_PATCH_). 
  * `api/users/{id}/subscribe/` - Подписаться на пользователя с соответствующим **id** или отписаться от него. (_GET, DELETE_).
  * `api/users/subscribe/subscriptions/` - Просмотр пользователей на которых подписан текущий пользователь. (_GET_).
  * 

* #### _Аутентификация и создание новых пользователей :point_down:_:
  * `api/auth/token/login/` - Получение токена (_POST_).
  * `api/auth/token/logout/` - Удаление токена (_POST_).

## _Алгоритм регистрации пользователей_:
1. Пользователь отправляет POST-запроc для регистрации нового пользователя с параметрами ***email*** ***username*** ***first_name*** ***last_name*** ***password*** на эндпоинт `/api/users/`.
2. Пользователь отправляет POST-запрос со своими регистрационными данными ***email*** ***password*** на эндпоинт `/api/token/login/` , в ответе на запрос ему приходит auth-token.
***Примечание***: При взаимодействии с фронтэндом приложения операция два происходит под капотом при переходе по эндпоинту `/api/token/login/`

## _Примеры выполнения запросов_:
##### Получение токена 
`api/auth/token/login/`
>
>Payload
>```json
>{
>  "password": "string",
>  "email": "string"
>}
>```
>Response sample (status code = 201)
>```json
>{
>"auth_token": "string"
>}
>```


##### Получение списка всех рецептов 
`api/recipes/`
>
>Response sample (status code = 200)
>```json
>{
>  "count": 123,
>  "next": "http://foodgram.example.org/api/recipes/?page=4",
>  "previous": "http://foodgram.example.org/api/recipes/?page=2",
>  "results": [
>    {
>      "id": 0,
>      "tags": [
>        {
>          "id": 0,
>          "name": "Завтрак",
>          "color": "#E26C2D",
>          "slug": "breakfast"
>        }
>      ],
>      "author": {
>        "email": "user@example.com",
>        "id": 0,
>        "username": "string",
>        "first_name": "Вася",
>        "last_name": "Пупкин",
>        "is_subscribed": false
>      },
>      "ingredients": [
>        {
>          "id": 0,
>          "name": "Картофель отварной",
>          "measurement_unit": "г",
>          "amount": 1
>        }
>      ],
>      "is_favorited": true,
>      "is_in_shopping_cart": true,
>      "name": "string",
>      "image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
>      "text": "string",
>      "cooking_time": 1
>    }
>  ]
>}
>```


##### Создание рецепта.
``api/recipes/`` (*требуется Аутентификация*)
>
>Payload
>```json
>{
>  "ingredients": [
>    {
>      "id": 1123,
>      "amount": 10
>    }
>  ],
>  "tags": [
>    1,
>    2
>  ],
>  "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
>  "name": "string",
>  "text": "string",
>  "cooking_time": 1
>}
>```
>Response sample (status code = 201)
>```json
>{
>  "id": 0,
>  "tags": [
>    {
>      "id": 0,
>      "name": "Завтрак",
>      "color": "#E26C2D",
>      "slug": "breakfast"
>    }
>  ],
>  "author": {
>    "email": "user@example.com",
>    "id": 0,
>    "username": "string",
>    "first_name": "Вася",
>    "last_name": "Пупкин",
>    "is_subscribed": false
>  },
>  "ingredients": [
>    {
>      "id": 0,
>      "name": "Картофель отварной",
>      "measurement_unit": "г",
>      "amount": 1
>    }
>  ],
>  "is_favorited": true,
>  "is_in_shopping_cart": true,
>  "name": "string",
>  "image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
>  "text": "string",
>  "cooking_time": 1
>}
>```

## Автор проекта
#### Капкаев Андрей
>*Улыбайтесь - это всех раздражает :relaxed:.*

