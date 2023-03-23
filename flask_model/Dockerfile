FROM python:3.9.7
WORKDIR /app
COPY ./requirements.txt /app
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
ENV FLASK_APP=app.py
ENV FLASK_DEBUG=1
CMD ["flask", "run", "--host", "0.0.0.0"]

