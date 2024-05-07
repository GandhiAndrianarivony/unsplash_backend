FROM python:3.11-slim-bullseye

ENV PIP_DISABLE_PIP_VERSION CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /apps

COPY ./requirements.txt .
RUN pip install -r requirements.txt
RUN pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

COPY ./entrypoint.sh .
RUN chmod +x ./entrypoint.sh

COPY . .