FROM python:3.9.7

LABEL authors='Andrey Kapkaev' version=1.0

WORKDIR /code

COPY requirements.txt .

RUN python -m pip install --upgrade pip

RUN pip3 install -r requirements.txt

COPY . .
