install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

test:
	python -m pytest scripts/test_sql.py

format:	
	black *.py 

lint:
	pylint --disable=R,C --ignore-patterns=test_.*?py scripts/*.py 

all: install lint test format deploy
