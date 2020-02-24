docker build .
docker-compose.yml
docker-compose build
docker-compose run app sh -c "django-admin.py startproject app ."
docker-compose run app sh -c "python manage.py test && flake8"
docker-compose run app sh -c "python manage.py startapp core"
AUTH_USER_MODEL
USERNAME_FIELD = 'email'
docker-compose run app sh -c "python manage.py makemigrations"
"python manage.py wait_for_db &&
python manage.py migrate &&
python manage.py runserver 0.0.0.0:8000"
docker-compose up
docker-compose run app sh -c "python manage.py createsuperuser"