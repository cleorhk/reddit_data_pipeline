import os
import praw
import pandas as pd
import psycopg2
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Reddit API credentials from .env
reddit = praw.Reddit(
    client_id=os.getenv('CLIENT_ID'),
    client_secret=os.getenv('CLIENT_SECRET'),
    user_agent=os.getenv('USER_AGENT')
)

# Extract posts from a subreddit
def extract_reddit_posts(subreddit_name, limit=100):
    subreddit = reddit.subreddit(subreddit_name)
    posts = []

    for post in subreddit.hot(limit=limit):
        posts.append({
            'title': post.title,
            'score': post.score,
            'id': post.id,
            'url': post.url,
            'comms_num': post.num_comments,
            'created': post.created,
            'body': post.selftext
        })

    return pd.DataFrame(posts)

# Save the extracted data to a CSV file
def save_to_csv(df, filename='data/reddit_posts.csv'):
    df.to_csv(filename, index=False)

# Transform data (example: convert timestamp to readable date)
def transform_data(df):
    df['created'] = pd.to_datetime(df['created'], unit='s')
    return df

# Load transformed data into PostgreSQL
def load_to_postgresql(df, table_name='reddit_posts'):
    try:
        conn = psycopg2.connect(
            dbname=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT')
        )
        cur = conn.cursor()

        for _, row in df.iterrows():
            cur.execute(f"""
                INSERT INTO {table_name} (title, score, post_id, url, comms_num, created, body)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (row['title'], row['score'], row['id'], row['url'], row['comms_num'], row['created'], row['body']))

        conn.commit()
        cur.close()
        conn.close()
        print(f"Data loaded successfully into {table_name}!")
    except Exception as e:
        print(f"Error: {e}")

# Main function to run the pipeline
def run_pipeline(subreddit_name='learnpython'):
    print("Extracting data...")
    df = extract_reddit_posts(subreddit_name)
    print(f"Data extracted. {len(df)} posts found.")

    print("Saving data to CSV...")
    save_to_csv(df)

    print("Transforming data...")
    df = transform_data(df)

    print("Loading data to PostgreSQL...")
    load_to_postgresql(df)

if __name__ == "__main__":
    run_pipeline('learnpython')
