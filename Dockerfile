FROM python:3.9.17-bullseye

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential

COPY requirements.txt .

RUN pip install -r requirements.txt

RUN pip install uwsgi

COPY . .

COPY .env .

EXPOSE 5000

CMD ["uwsgi", "--ini", "uwsgi.ini"]