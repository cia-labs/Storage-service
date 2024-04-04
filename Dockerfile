# Use an official Python runtime as a parent image
FROM python:3.10-slim
# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# app vars
ENV STORAGE_DIRECTORY /data
ENV DB_FILE /data/data.db

RUN mkdir /data

# Set work directory
WORKDIR /server

# Install dependencies
COPY server/requirements.txt /server/
RUN pip3 install --no-cache-dir -r requirements.txt
RUN apt-get update
RUN apt install sqlite3 -y

# Copy project
COPY server/ /server/

# Command to run the uvicorn server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]