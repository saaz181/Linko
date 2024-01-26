# Use an official Python runtime as a parent image
FROM python:3.10

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

COPY requirements.txt /app/

# Update/Install General Packages
RUN apt-get update \
    && apt-get install -y libmariadb-dev \
    && apt-get install -y python3-pip \
    && apt-get install -y build-essential \
    && apt-get install -y libcurl4-openssl-dev \
    && apt-get install -y libssl-dev \
    && pip3 install --upgrade pip

# Install any needed packages specified in requirements.txt
RUN pip3 install -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

# Create a startup script
COPY run.sh /app/run.sh

# Run app.py when the container launches
CMD ["sh", "/app/run.sh"]
