FROM python:3.9-slim

WORKDIR /app

COPY payment_service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY payment_service/ ./payment_service/
COPY common/ ./common/

EXPOSE 8000
CMD ["uvicorn", "payment_service.main:app", "--host", "0.0.0.0", "--port", "8000"]
