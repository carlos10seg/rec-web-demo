# FROM ubuntu:18.04

# RUN apt-get update -y && \
#     apt-get install -y python3.6-dev
FROM python:3.8-buster

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /demoapp/requirements.txt

WORKDIR /demoapp

RUN pip install -r requirements.txt

COPY . /demoapp

EXPOSE 5002

# ENTRYPOINT ["python"]
# CMD ["app.py"]
CMD ["python", "app.py"]