# Git
> git pull

### git push step
> git add .
> git commit -am "commit message"
> git push



# Setup Python
> python3 -m venv venv

> source venv/bin/activate

> pip install --upgrade pip

> pip install "Django>=4,<5" Pillow mysql-connector-python requests


# Start Project Django
> django-admin startproject core_project .

# Start app
> python manage.py startapp app_name

# Docker
> docker-compose up --build
> docker-compose down

> docker-compose exec web python manage.py migrate --noinput
> docker-compose exec web python manage.py createsuperuser
> docker-compose exec web python manage.py makemigrations app_name
> docker-compose exec web python manage.py migrate app_name

> docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --no-input --clear