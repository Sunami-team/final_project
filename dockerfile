FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /root

COPY requirements.txt /root/
RUN pip install -r requirements.txt

COPY . /root