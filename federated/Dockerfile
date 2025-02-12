FROM python:3.9-slim

WORKDIR /app

# Copy the federated.py file into the container
COPY federated.py .

# Install required package
RUN pip install --no-cache-dir pika

CMD ["python", "federated.py"]
