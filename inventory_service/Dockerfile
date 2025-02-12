FROM python:3.9-slim

WORKDIR /app

COPY inventory_service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY inventory_service/ ./inventory_service/
COPY common/ ./common/

EXPOSE 8000
CMD ["uvicorn", "inventory_service.main:app", "--host", "0.0.0.0", "--port", "8000"]
