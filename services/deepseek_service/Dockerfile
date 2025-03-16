FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1  

ENV PYTHONUNBUFFERED=1


RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    gcc \
    libpq-dev \
    curl \
    && apt-get clean

WORKDIR /app
COPY requirements.txt /app/
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8001

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8001"]