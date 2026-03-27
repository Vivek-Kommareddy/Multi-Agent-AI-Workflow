install:
	pip install -r requirements.txt

dev:
	uvicorn src.api.main:app --reload

research:
	python -m examples.simple_research

serve:
	uvicorn src.api.main:app --host 0.0.0.0 --port 8000

demo:
	streamlit run src/ui/streamlit_app.py

test:
	MOCK_TOOLS=true MOCK_LLM=true pytest -q

lint:
	ruff check . && mypy src

docker-up:
	docker compose up --build
