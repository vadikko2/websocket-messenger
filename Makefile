all: run

install:
	@echo "Copying requirements.txt to requirements.tmp.txt"
	@if [ -f ./requirements.txt ]; then \
	cp requirements.txt requirements.tmp.txt; \
	else \
	@echo "requirements.txt not found!"; \
	exit 1; \
	fi

	@echo "Replacing GitHub URL with token"
	@sed -i '' "s|https://github.com/vadikko2|https://$(GITHUB_TOKEN)@github.com/vadikko2|g" requirements.tmp.txt

	@echo "Installing requirements"
	@bash -c "source ./venv/bin/activate; pip install --no-cache-dir -r requirements.tmp.txt --root-user-action=ignore"

	@echo "Cleaning up temporary file"
	@rm -f requirements.tmp.txt

dev:
	@echo "Copying requirements.txt to requirements.tmp.txt"
	@if [ -f ./requirements.txt ]; then \
	cp requirements.txt requirements.tmp.txt; \
	else \
	@echo "requirements.txt not found!"; \
	exit 1; \
	fi

	@echo "Copying requirements-dev.txt to requirements-dev.tmp.txt"
	@if [ -f ./requirements-dev.txt ]; then \
	cp requirements-dev.txt requirements-dev.tmp.txt; \
	else \
	@echo "requirements-dev.txt not found!"; \
	exit 1; \
	fi

	@echo "Replacing GitHub URL with token"
	@sed -i '' "s|https://github.com/vadikko2|https://$(GITHUB_TOKEN)@github.com/vadikko2|g" requirements.tmp.txt
	@echo "Replacing requirements file path with token"
	@sed -i '' "s|requirements.txt|requirements.tmp.txt|g" requirements-dev.tmp.txt

	@echo "Installing requirements-dev"
	@bash -c "source ./venv/bin/activate; pip install --no-cache-dir -r requirements-dev.tmp.txt --root-user-action=ignore"

	@echo "Cleaning up temporary files"
	@rm -f requirements.tmp.txt
	@rm -f requirements-dev.tmp.txt

run: install
	@echo "Starting the application"
	@bash -c "source ./venv/bin/activate; uvicorn --app-dir src/ presentation.api.main:app --workers 1 --host 0.0.0.0 --port 80"

docker-up:
	@echo "Starting the application in docker"
	@docker-compose up --build -d

docker-down:
	@echo "Stopping the docker containers application"
	@docker-compose down

pre-commit: dev
	@echo "Starting pre-commit"
	@bash -c "source ./venv/bin/activate; pre-commit install; pre-commit run --all-files --show-diff-on-failure"

.PHONY: run install
