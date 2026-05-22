FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir psycopg2-binary datasets ragas
CMD ["python", "evaluate.py"]
