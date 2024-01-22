# Use an official Python runtime as a parent image
FROM python:3.10.11

# Set the working directory in the container
WORKDIR /nflapp

# Copy the requirements file into the container
COPY requirements.txt ./

# Install dependencies in the container
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django project into the container
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Define the command to run your application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]