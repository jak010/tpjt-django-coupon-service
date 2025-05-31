export DJANGO_SETTINGS_MODUEL=config.settings.local

docker.run:
	 docker-compose -f ./.docker/docker-compose.yml up

run.local:
	 python manage.py runserver --settings=$(DJANGO_SETTINGS_MODUEL)

app.migrations:
	python manage.py makemigrations --settings=$(DJANGO_SETTINGS_MODUEL)

app.migrate:
	python manage.py migrate --settings=$(DJANGO_SETTINGS_MODUEL)

