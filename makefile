export DJANGO_SETTINGS_MODUEL=config.settings.local

docker.run:
	 docker-compose -f ./.docker/docker-compose.yml up

run.local:
	 python manage.py runserver --settings=$(DJANGO_SETTINGS_MODUEL)

app.migrations:
	python manage.py makemigrations --settings=$(DJANGO_SETTINGS_MODUEL)

app.migrate:
	python manage.py migrate --settings=$(DJANGO_SETTINGS_MODUEL)

app.deploy:
	gunicorn config.wsgi:application --workers 8 --log-level debug --error-logfile gunicorn-error.log

load.test.v0:
	 locust -f ./tests/locust-coupon-issue-v0.py --host=http://localhost:8000
