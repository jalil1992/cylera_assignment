VENV := ./venv
VENV_PYTHON := $(VENV)/bin/python3
VENV_PIP := $(VENV)/bin/pip3

venv:
	python3 -m venv $(VENV)

install:
	$(VENV_PIP) install -r requirements.txt

setup: venv install

clean:
	rm -rf $(VENV)

format:
	PYTHONPATH=. $(VENV_PYTHON) -m black .

test:
	PYTHONPATH=checkoutbot $(VENV_PYTHON) -m pytest

api:
	$(VENV_PYTHON) checkoutbot/api.py

generate_fast:
	$(VENV_PYTHON) checkoutbot/generator.py --with-checkout --customer-count 50 --item-count 100 --event-count 250

generate:
	$(VENV_PYTHON) checkoutbot/generator.py --with-checkout

json:
	$(VENV_PYTHON) checkoutbot/generator.py --with-checkout --to-json --dry-run
	npx -y prettier --write *.json
