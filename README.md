# Video Management API
This project provides a REST API for video management using FastAPI. It includes functionalities for uploading videos, converting them to `.mp4` format, searching videos by metadata, and blocking video downloads based on a blocklist.

## Project Overview

1. **Video Upload**: An API endpoint to upload videos, convert them to `.mp4` format, and store them.
2. **Video Search**: An API endpoint to search videos by metadata such as name and size.
3. **Blocklist**: A caching mechanism to prevent downloads of videos that are in a blocklist.
4. **OOP Design**: The code uses Object-Oriented Programming principles to manage functions and classes.
5. **Unit Tests**: Unit tests are provided for each API endpoint.
6. **Dockerization**: Docker files are provided to containerize the FastAPI application, PostgreSQL database, and caching system.
7. **Deployment**: Instructions for deploying the application on an EC2 instance.

## Project Structure

```
video_management/
├── app/
│   ├── api/
│   │   ├── router.py
│   ├── core/
│   │   └── config.py
│   ├── dao/
│   │   └── dao.py
│   ├── models/
│   │   └── models.py
│   ├── schemas/
│   │   └── videos.py
│   ├── services/
│   │   └── video_service.py
│   ├── main.py
├── tests/
│   ├── test_api.py
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

# Installation

1. Clone the Repository*

   ```bash
   git clone https://github.com/sanyog2491/mi_task
   cd mi_task
   ```

2. Install Dependencies

   Create a virtual environment and install the required Python packages.

   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

# Configuration

1. Database and Caching Configuration

   Update the `app/core/config.py` file with your PostgreSQL and caching configuration.

   # app/core/config.py
   DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost/mi_db"
   REDIS_URL = "redis://localhost:6379/0"

2. Docker Configuration

   Ensure Docker and Docker Compose are installed. Use the provided Dockerfiles and `docker-compose.yml` for containerization.

# Running the Application

1. Using Docker Compose

   docker-compose up --build


   This will start FastAPI, PostgreSQL, and Redis services.

2. Without Docker

   Start the application locally:

   uvicorn app.main:app --reload


# API Endpoints

1. Upload Video

   - Endpoint: `POST api/upload/`
   - Description: Uploads a video, converts it to `.mp4`, and stores it.
   - Request Body: Form-data with a `file` field.
   - Response: Details of the uploaded video.

2. Search Videos

   - Endpoint: `GET /search/`
   - Description: Searches videos by name and size.
   - Query Parameters:
     - `name` (optional): The name of the video.
     - `size` (optional): The size of the video.
   - Response: List of videos matching the search criteria.

3. Block Video

   - Endpoint: `POST /block/`
   - Description: Adds a video ID to the blocklist.
   - Request Body: JSON with `video_id` field.

4. Unblock Video

   - Endpoint: `POST /unblock/`
   - Description: Removes a video ID from the blocklist.
   - Request Body: JSON with `video_id` field.

# Unit Tests

To run the unit tests:

pytest


# Deployment on EC2

1. Set Up EC2 Instance

   Launch an EC2 instance with your preferred Linux distribution.

2. Install Docker and Docker Compose

   Follow the Docker installation instructions for your Linux distribution.

3. Deploy the Application

   - Transfer your Docker files and `docker-compose.yml` to the EC2 instance.
   - Build and start the containers using:

     docker-compose up --build

# Notes

- Ensure that all necessary environment variables and configurations are set before running the application.
- For video conversion, ensure you have `ffmpeg` installed in the Docker container or in the system where FastAPI is running.
