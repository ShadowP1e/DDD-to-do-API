FROM python:3.11-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY ./run.sh .

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod +x ./run.sh

EXPOSE 8000

ENTRYPOINT ["./run.sh"]