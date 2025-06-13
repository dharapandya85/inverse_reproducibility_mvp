FROM python:3.9-slim-buster

WORKDIR /app

# Copy generated requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create directories for data and results
RUN mkdir -p /app/output/reproduced_results/figures
RUN mkdir -p /app/output/reproduced_results/tables


# Copy the generated code script
COPY reproduced_code.py /app/reproduced_code.py

CMD ["python", "reproduced_code.py"]