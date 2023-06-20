run:
	python3 manage.py runserver
	
migrate:
	python3 manage.py makemigrations
	python3 manage.py migrate

user:
	python3 manage.py createsuperuser
	
start:
	django-admin startproject main .

celery:
	celery -A main worker -l debug

celery_beat:
	celery -A main beat

restart:
	sudo systemctl daemon-reload
	sudo systemctl restart gunicorn
	sudo nginx -t && sudo systemctl restart nginx

restart_celery:
	sudo supervisorctl reread
	sudo supervisorctl update
	sudo supervisorctl