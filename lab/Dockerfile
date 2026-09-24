FROM python:3.14-slim-bookworm

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

RUN useradd --create-home --uid 1000 app

COPY app/ ./app/
RUN chown -R app:app /app

USER app

EXPOSE 8080

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
