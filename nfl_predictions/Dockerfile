# Use an official Python runtime as a parent image
FROM python:3.11.7

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /nflapp

# Copy the current directory contents into the container at /app
COPY . /nflapp

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]