FROM python:buster
RUN apt-get update
RUN apt-get install virtualenv -y
WORKDIR /app
RUN virtualenv venv
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=127.0.0.1:5000"]