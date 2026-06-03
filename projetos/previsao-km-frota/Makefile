.PHONY: install train test predict

install:
	pip install -r requirements.txt

train:
	python -m mkm.train

test:
	pytest -q

predict:
	@echo "uso: python -m mkm.predict --placa ABC1A23 --data 2026-12-31"
