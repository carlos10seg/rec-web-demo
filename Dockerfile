# FROM ubuntu:18.04

# RUN apt-get update -y && \
#     apt-get install -y python3.6-dev
FROM python:3.8-buster

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

EXPOSE 5010

# ENTRYPOINT ["python"]
# CMD ["app.py"]
CMD ["python", "app.py"]