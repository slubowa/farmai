
FROM python:3.9-slim

WORKDIR /usr/src/app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        libc6-dev \
        g++ \
    && rm -rf /var/lib/apt/lists/*

COPY setup.py ./

RUN pip install --no-cache-dir -e .

COPY . .

COPY .env ./

ENV FLASK_APP=app.py \
    FLASK_ENV=production

EXPOSE 5001

CMD ["flask", "run", "--host=0.0.0.0"]