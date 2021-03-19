requirements:
	pipenv lock
	pipenv lock -r > requirements.txt
	pipenv lock -r --dev-only > requirements-dev.txt
