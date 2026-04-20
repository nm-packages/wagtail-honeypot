.DEFAULT_GOAL := help

.PHONY: help sync lint format run mail test tox migrate superuser

help:
	@printf "Available targets:\n"
	@printf "  make sync        Sync the uv-managed development environment\n"
	@printf "  make lint        Run Ruff lint checks\n"
	@printf "  make format      Run Ruff formatting\n"
	@printf "  make run         Start the local Django development server\n"
	@printf "  make mail        Start Mailhog for local email testing\n"
	@printf "  make test        Run the default Django test suite with coverage\n"
	@printf "  make tox         Run the supported compatibility matrix\n"
	@printf "  make migrate     Apply local database migrations\n"
	@printf "  make superuser   Create the default local admin user\n"

sync:
	uv sync

lint:
	uv run ruff check .

format:
	uv run ruff format .

run:
	uv run python manage.py runserver 0:8000

mail:
	docker run -p 8025:8025 -p 1025:1025 mailhog/mailhog

test:
	uv run coverage run manage.py test
	uv run coverage report

tox:
	uv run tox --skip-missing-interpreters

migrate:
	uv run python manage.py migrate

superuser:
	@echo "from django.contrib.auth import get_user_model; get_user_model().objects.create_superuser('admin', 'admin@admin.com', 'changeme')" | uv run python manage.py shell
