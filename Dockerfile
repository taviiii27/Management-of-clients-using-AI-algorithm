FROM python:3.13-slim

WORKDIR  /api

COPY . /api

RUN pip install -r requirements.txt

CMD ["python", "api.py"]




