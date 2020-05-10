FROM python:3.8-alpine

WORKDIR /usr/app
COPY app/py-twit.py log.conf requirements.txt app ./
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8000/tcp
VOLUME /usr/app/db

CMD ["python", "py-twit.py"]