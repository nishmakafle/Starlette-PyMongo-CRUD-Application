#Specify the Base Image
FROM python:3.9-slim 
#Set the Working Directory
WORKDIR /app


# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 0

#Copy the Project Files

COPY . /app

COPY requirements .

RUN pip install -r requirements.txt



