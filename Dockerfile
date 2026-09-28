FROM python:3.11-slim

RUN pip install --no-cache-dir uv==0.8.13

WORKDIR /code

COPY ./pyproject.toml ./app ./app

RUN uv pip install --system -r app/requirements.txt

EXPOSE 8080

CMD ["uvicorn", "app.fast_api_app:fast_api_app", "--host", "0.0.0.0", "--port", "8080"]
