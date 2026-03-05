.PHONY: help install test run clean lint format security

help:
	@echo "Available commands:"
	@echo "  make install    - Install dependencies"
	@echo "  make test       - Run tests"
	@echo "  make run        - Run the script (preview mode)"
	@echo "  make run-unfollow - Run and actually unfollow"
	@echo "  make clean      - Clean cache files"
	@echo "  make lint       - Run linter"
	@echo "  make format     - Format code with black"
	@echo "  make security   - Run security checks"

install:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

test:
	pytest tests/ -v --cov=. --cov-report=term-missing

run:
	python unfollow_nonfollowers.py

run-unfollow:
	python unfollow_nonfollowers.py --unfollow

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name "dist" -exec rm -rf {} +
	find . -type d -name "build" -exec rm -rf {} +

lint:
	flake8 unfollow_nonfollowers.py tests/
	mypy unfollow_nonfollowers.py --ignore-missing-imports

format:
	black unfollow_nonfollowers.py tests/

security:
	bandit -r unfollow_nonfollowers.py
	safety check
