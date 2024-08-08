import os
from dotenv import load_dotenv
import praw
import json
import datetime

load_dotenv()

def fetch_reddit_data(subreddit, keyword, start_date, end_date, reddit):
    start_timestamp = int(start_date.timestamp())
    end_timestamp = int(end_date.timestamp())
    
    comments = []
    for comment in reddit.subreddit(subreddit).comments(limit=None):
        if start_timestamp <= comment.created_utc <= end_timestamp:
            if keyword.lower() in comment.body.lower() or keyword == '':
                comments.append({
                    'id': comment.id,
                    'body': comment.body,
                    'created_utc': comment.created_utc,
                    'author': str(comment.author),
                    'score': comment.score,
                    'permalink': comment.permalink,
                })
    return comments

def save_data_to_file(data, filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def main():
    subreddit = input("Enter the subreddit to search: ")
    keyword = input("Enter the keyword to search for (press Enter to skip): ")
    
    start_date_str = input("Enter the start date (YYYY-MM-DD): ")
    end_date_str = input("Enter the end date (YYYY-MM-DD): ")

    start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d')
    end_date = datetime.datetime.strptime(end_date_str, '%Y-%m-%d')
    
    output_filename = f'data/raw/reddit_data_{subreddit}{"_" + keyword if keyword else ""}_{start_date_str}_to_{end_date_str}.json'
    
    reddit = praw.Reddit(
        client_id=os.getenv('REDDIT_CLIENT_ID'),
        client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
        user_agent=os.getenv('REDDIT_USER_AGENT')
    )
    
    data = fetch_reddit_data(subreddit, keyword, start_date, end_date, reddit)
    
    save_data_to_file(data, output_filename)
    
    print(f"Fetched {len(data)} comments from subreddit '{subreddit}' containing keyword '{keyword}'" if keyword else f"Fetched {len(data)} comments from subreddit '{subreddit}'")

if __name__ == "__main__":
    main()
