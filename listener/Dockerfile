FROM python:2

COPY . /app
WORKDIR /app

RUN apt-get update
RUN apt-get install python-pip python-dev -y

RUN pip install -r requirements.txt

ENV PROCESSOR_ENDPOINT 'http://processor:8000/'
ENV PORT 8001
ENV DEBUG_MODE 1

CMD ["/bin/sh", "-c", "gunicorn app:app --config=config.py"]