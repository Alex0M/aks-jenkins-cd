FROM python:3.6.2

COPY /app/ /usr/app
WORKDIR /usr/app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]

CMD ["main.py"]