# pull official base Python Docker image
FROM python:3.12.3

# set env variables
# prevent from writing out pyc files
ENV PYTHONDONTWRITEBYTECODE=1
# stdout and stderr are sent to the terminal without first being buffered
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /code

# Install dependencies
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the Django project
COPY . .