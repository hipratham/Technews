pip install -r requirements-prod.txt
python manage.py collectstatic --noinput
python manage.py migrate
