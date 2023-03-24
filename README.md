![Workflow](https://github.com/andrewlegkii/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)


# Описание проекта YaMDb  

Проект YaMDb собирает отзывы (Review) пользователей на произведения (Titles). Произведения делятся на категории: «Книги», «Фильмы», «Музыка». Список категорий (Category) может быть расширен администратором.  

Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.
В каждой категории есть произведения: книги, фильмы или музыка. Например, в категории «Книги» могут быть произведения «Винни-Пух и все-все-все» и «Марсианские хроники», а в категории «Музыка» — песня «Давеча» группы «Насекомые» и вторая сюита Баха.    

Произведению может быть присвоен жанр (Genre) из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»). Новые жанры может создавать только администратор.  

Пользователи оставляют к произведениям текстовые отзывы (Review) и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число). На одно произведение пользователь может оставить только один отзыв.  

### Технологии испльзуемые в проекте 
* Python 3.7
* Django REST framework 3.12.4
* Git
* SQLite3  

### Запуск проекта  
Cоздать и активировать виртуальное окружение:  

`python -m venv venv  `
    
`source venv/Scripts/activate`  

Установить зависимости из файла requirements.txt:  

`pip install -r requirements.txt`  

В главной папке проекта (api_yamdb) выполнить миграции:  

`python manage.py migrate`  

Запустить проект:  

`python manage.py runserver`  


### Пользовательские роли
* Аноним — может просматривать описания произведений, читать отзывы и комментарии.  
* Аутентифицированный пользователь (user) — может читать всё, как и Аноним, может публиковать отзывы и ставить оценки произведениям (фильмам/книгам/песенкам), может комментировать отзывы; может редактировать и удалять свои отзывы и комментарии, редактировать свои оценки произведений. Эта роль присваивается по умолчанию каждому новому пользователю.  
* Модератор (moderator) — те же права, что и у Аутентифицированного пользователя, плюс право удалять и редактировать любые отзывы и комментарии.  
* Администратор (admin) — полные права на управление всем контентом проекта. Может создавать и удалять произведения, категории и жанры. Может назначать роли пользователям.  
* Суперюзер Django должен всегда обладать правами администратора, пользователя с правами admin. Даже если изменить пользовательскую роль суперюзера — это не лишит его прав администратора. Суперюзер — всегда администратор, но администратор — не обязательно суперюзер.  

### Самостоятельная регистрация новых пользователей
1. Пользователь отправляет POST-запрос с параметрами email и username на эндпоинт `/api/v1/auth/signup/`.
2. Сервис YaMDB отправляет письмо с кодом подтверждения (`confirmation_code`) на указанный адрес email.
3. Пользователь отправляет POST-запрос с параметрами `username` и `confirmation_code` на эндпоинт `/api/v1/auth/token/`, в ответе на запрос ему приходит `token` (JWT-токен).  

В результате пользователь получает токен и может работать с API проекта, отправляя этот токен с каждым запросом.
После регистрации и получения токена пользователь может отправить PATCH-запрос на эндпоинт `/api/v1/users/me/` и заполнить поля в своём профайле (описание полей — в документации).

## Поверка проекта
[WEB Django REST framework](http://84.201.167.194/api/v1/) (Сейчас сервер перестал запускаться, могу Вам написать в пачке? Сейчас вот такая ошибка при запуске. Уже все перепробовал: name: yamdb_workflow

on: [push]

jobs:
  tests:
    name: Clone, setup and test
    runs-on: ubuntu-latest

    strategy:
      matrix:
        python-version: ["3.7"]

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v3
      with:
        python-version: ${{ matrix.python-version }}

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip 
        pip install flake8 pep8-naming flake8-broken-line flake8-return flake8-isort
        pip install -r api_yamdb/requirements.txt

    - name: Test with flake8 and django tests
      run: |
        python -m flake8
        pytest

  build_and_push_to_docker_hub:
    name: Push Docker image to Docker Hub
    runs-on: ubuntu-latest
    needs: tests
    if: github.ref_name == 'master'
    steps:
      - name: Check out the repo
        uses: actions/checkout@v3

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v1

      - name: Login to Docker 
        uses: docker/login-action@v1 
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}

      - name: Push to Docker Hub
        uses: docker/build-push-action@v2
        with:
          push: true
          tags: andrewlegki/yamdb_final
          file: api_yamdb/Dockerfile

  deploy:
    name: Deploy on Yandex.Cloud
    runs-on: ubuntu-latest
    needs: build_and_push_to_docker_hub
    steps:
    - name: executing remote ssh commands to deploy
      uses: appleboy/ssh-action@master
      with:
        host: ${{ secrets.HOST }}
        username: ${{ secrets.USER }}
        key: ${{ secrets.SSH_KEY }}
        passphrase: ${{ secrets.PASSPHRASE }}
        script: |
          sudo docker-compose pull andrewlegkii/yamdb
          sudo docker-compose stop
          sudo docker-compose rm -f web
          touch .env
          echo DB_ENGINE=${{ secrets.DB_ENGINE }} >> .env
          echo DB_NAME=${{ secrets.DB_NAME }} >> .env
          echo POSTGRES_USER=${{ secrets.POSTGRES_USER }} >> .env
          echo POSTGRES_PASSWORD=${{ secrets.POSTGRES_PASSWORD }} >> .env
          echo DB_HOST=${{ secrets.DB_HOST }} >> .env
          echo DB_PORT=${{ secrets.DB_PORT }} >> .env
          echo SECRET_KEY=${{ secrets.SECRET_KEY }} >> .env
          echo ALLOWED_HOSTS=${{ secrets.ALLOWED_HOSTS }} >> .env
          sudo docker-compose up -d

  send_message:
    name: Send message to Telegram
    runs-on: ubuntu-latest
    needs: deploy
    steps:
    - name: send message
      uses: appleboy/telegram-action@master
      with:
        to: ${{ secrets.TELEGRAM_TO }}
        token: ${{ secrets.TELEGRAM_TOKEN }}
        message: ${{ github.workflow }} успешно выполнен!
)