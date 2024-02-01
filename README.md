# NFL Game Winner Prediction

## Overview
This project aims to predict the outcome of NFL games using a machine learning model. It leverages logistic regression to analyze play-by-play data and other significant features to forecast game winners. The application is built on Django, utilizing HTML, CSS, and JavaScript for the frontend, and is served via Nginx. The entire application is containerized using Docker for ease of deployment and scalability.

## Features
**Machine Learning Model**: Utilizes logistic regression to predict NFL game winners based on historical play-by-play data.  
  
**Data Scraping and Processing**: Automated AWS Lambda functions for scraping weekly NFL data, storing it in an S3 bucket, and then processing this data into an Amazon RDS database.  
  
**Exploratory Data Analysis**: Conducted to identify key features and trends within the NFL game data to inform the model.  
  
**Web Application**: A Django-based web application with a user-friendly interface for displaying predictions.  
  
**Deployment**: The application is containerized using Docker and deployed on an AWS EC2 instance for robust, scalable access.  
  
**Database**: Uses Amazon RDS for reliable, scalable storage of game data, which is updated on a weekly basis.  

## Technology Stack
Frontend: HTML, CSS, JavaScript
Backend: Django
Web Server: Nginx
Containerization: Docker
Cloud: AWS (EC2, RDS, S3, Lambda)
Database: Amazon RDS
Machine Learning: Python, Logistic Regression

## Getting Started
Prerequisites
Docker
AWS CLI (configured with your AWS account)
Python 3.x

## Usage
Access the web application via http://ec2-xx-xx-xx-xx.compute-1.amazonaws.com.
Select a week to view predictions for upcoming NFL games.

## Data Pipeline
1. Data Scraping: AWS Lambda function is triggered weekly to scrape play-by-play data.
2. Data Storage: Raw data is stored in an S3 bucket.
3. Data Transformation: Another Lambda function processes the raw data and updates the RDS database.
