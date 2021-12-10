FROM python:3.9

WORKDIR /code
COPY requirements.txt .
RUN python pip install --upgrade pip
RUN pip3 install -r requirements.txt
COPY . .

