# FarmAI Platform

## Introduction
FarmAI is designed to help farmers with credit scoring and fertilizer recommendations, enhancing agricultural productivity and financial management.
## Prerequisites
Before you begin, ensure you have installed:
* Docker ([Installation guide](https://docs.docker.com/get-docker/))
* The .env with API keys will be shared separately

## Installation
Clone the FarmAI repository by running:
* git clone https://github.com/slubowa/farmai.git

## Environment variables
 *The .env file is critical as it contains the API keys. After cloning the repository, copy it as provided into the backend folder before running the application. If you do not have access to this file you have create your own .env file with api keys for open AI, Nomatim, open weather and the flask app secret.

## Navigatee to the cloned repository
*cd farmai

## Running the Application
This application consists of a frontend and a backend, both containerized using Docker. Ensure that you have installed docker and it is running. Follow these steps to run the application:

1. Navigate to the backend folder and run
* docker build -t farmai-backend .
* docker run -p 5001:5000 farmai-backend
2. Open a different terminal window
3. Navigate to the Frontend folder and run:
* docker build -t farmai-frontend .
* docker run -p 3000:3000 farmai-frontend
## Usage
* Navigate to http://localhost:3000 on your browser to interact with the FarmAI platform. The application provides interfaces for credit scoring and fertilizer recommendations.
