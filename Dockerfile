FROM python:slim-bullseye

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install -y build-essential libgl1-mesa-glx libglib2.0-0 libsm6 libxrender1 libxext6 \
    && pip install --upgrade pip \
    && pip install -r requirements.txt \
    && apt-get purge -y --auto-remove build-essential \
    && rm -rf /var/lib/apt/lists/*

CMD ["python", "main.py"]