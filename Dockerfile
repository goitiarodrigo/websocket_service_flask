FROM python:3.9.17-bullseye

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "-w", "4" , "0.0.0.0:5000", "-b", "app:app"]