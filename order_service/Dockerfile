FROM python:3.9-slim

WORKDIR /app

# Copy requirements from the order_service folder
COPY order_service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the order_service code and the common package
COPY order_service/ ./order_service/
COPY common/ ./common/

EXPOSE 8000
CMD ["uvicorn", "order_service.main:app", "--host", "0.0.0.0", "--port", "8000"]
