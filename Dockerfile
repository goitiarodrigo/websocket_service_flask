FROM python:3.9.17-bullseye

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

COPY .env .

EXPOSE 5000

CMD ["python", "app.py", "--host=0.0.0.0"]