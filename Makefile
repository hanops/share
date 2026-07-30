.PHONY: check build serve

PYTHON ?= python3

check:
	$(PYTHON) scripts/check.py

build:
	$(PYTHON) scripts/build_sites.py

serve:
	$(PYTHON) -m http.server 8000 --bind 127.0.0.1
