FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04

WORKDIR /app

RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY app/requirements.txt .
RUN pip3 install --upgrade pip && pip3 install -r requirements.txt

CMD ["python3", "src/train.py"]
