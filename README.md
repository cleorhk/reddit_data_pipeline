# Reddit Data Pipeline
## Project Description
This project is a Python-based data pipeline that extracts data from Reddit using the Reddit API, transforms the data, and loads it into a PostgreSQL database. It does not use Docker or Airflow, but it leverages basic Python scripts to automate the ETL (Extract, Transform, Load) process.
## Features
- Extracts data from Reddit via the Reddit API.
- Stores the extracted data in a CSV file.
- Transforms and cleans the data.
- Loads the transformed data into a PostgreSQL database.
## Technologies Used
- Python
- Reddit API (via `praw` library)
- PostgreSQL
- Psycopg2 (for connecting to PostgreSQL)
- Pandas (for data manipulation)
## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/cleorhk/reddit_data_pipeline.git
cd reddit_data_pipeline
python3 -m venv venv
source venv/bin/activate  # For Windows: venv\Scripts\activate
touch .env
CLIENT_ID=your_reddit_client_id
CLIENT_SECRET=your_reddit_client_secret
USER_AGENT=your_reddit_user_agent
DB_HOST=your_postgresql_host
DB_NAME=your_postgresql_db_name
DB_USER=your_postgresql_username
DB_PASS=your_postgresql_password
