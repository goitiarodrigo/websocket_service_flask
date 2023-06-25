FROM python:3.9.17-bullseye

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential

COPY requirements.txt .

RUN pip install -r requirements.txt

RUN pip install uwsgi

COPY . .

EXPOSE 5000

CMD ["gunicorn", "-w", "4" , "0.0.0.0:5000", "-b", "app:app"]