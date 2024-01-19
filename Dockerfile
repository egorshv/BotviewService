FROM python:3.10
ENV TZ=Europe/Moscow
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PIP_ROOT_USER_ACTION=ignore
RUN apt-get update

RUN mkdir "/src"

WORKDIR /src

COPY requirements.txt .

RUN pip install --upgrade pip \
    && pip install --no-cache -r ./requirements.txt

COPY . .
