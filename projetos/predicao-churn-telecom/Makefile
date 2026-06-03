.PHONY: install train test

install:        ## Instala as dependências
	pip install -r requirements.txt

train:          ## Treina o modelo e gera métricas + figuras em reports/
	python -m churn.train

test:           ## Roda a suíte de testes
	pytest -q
