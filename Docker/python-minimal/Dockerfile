FROM python:3.8.1-slim-buster

# Install and update software
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
RUN apt-get upgrade -y

# Copy projects code
COPY . /opt/app
WORKDIR /opt/app
# RUN pip install -r requirements.txt --no-cache-dir

# Start app
ENTRYPOINT ["python"]
CMD ["app.py"]
