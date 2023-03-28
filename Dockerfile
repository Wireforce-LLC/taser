# This is a sample Dockerfile

# set base image python:3.8-slim-buster
FROM python:3.11-slim-buster

# set working directory as app
WORKDIR /app

# copy requirements.txt file from local (source) to file structure of container (destination)
COPY requirements.txt requirements.txt

# Install the requirements specified in file using RUN
RUN pip3 install -r requirements.txt

RUN apt-get -y update
RUN apt-get -y install git adb

# copy all items in current local directory (source) to current container directory (destination)
COPY . .

# command to run when image is executed inside a container
CMD [ "adb", "start-server", "&&", "python3", "main.py", "hybrid" ]