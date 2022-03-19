# base image to build customized docker image
FROM python:alpine3.10 
# set working directory inside docker
WORKDIR /app 
# copy requirement.txt from current directory to /app folder
COPY requirements.txt /app/requirements.txt
# load any necessary python packages specified in requirements.txt
# RUN: image build step - install packages inside image
RUN pip install -r requirements.txt
# informs Docker that the container listens on the specified network ports at runtime
# default protocol: TCP
EXPOSE 5000
# copy everything to /app
# if we change the code only, use this as a separate layer will be efficient
COPY . /app

# CMD, ENTRYPOINT: launch the python application
# CMD: what you pass from the command line will replace this instruction
# eg: docker build -t IMAGE_NAME:TAG_NAME ping google.com -> python ./app.py is replaced by ping google.com 
# CMD python ./app.py

# ENTRYPOINT: won't be replaced by whatever you pass from the command line unless we add a flag in `docker run`: --entrypoint
ENTRYPOINT ["python", "./app.py"]


# Reference
# 1. https://docs.docker.com/engine/reference/builder/#:~:text=EXPOSE&text=The%20EXPOSE%20instruction%20informs%20Docker,not%20actually%20publish%20the%20port.
# 2. https://stackoverflow.com/questions/37461868/difference-between-run-and-cmd-in-a-dockerfile
