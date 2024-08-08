Reddit Sentiment Analysis Bot

This bot fetches comments from a specific subreddit, and analyzes them for their sentiment and emotional weights. It can also identify the happiest, saddest, most subjective, and least subjective comments, as well as visualize the historical sentiment and emotion trends, and histograms and scatter plots of the sentiment data.

In order to use this bot, first clone the repository and install the dependencies with pip install -r requirements.txt. Then you will need to set up Reddit PRAW.
Go to this link: https://www.reddit.com/prefs/apps
Create a new script application and note down the client_id, client_secret, and user_agent. Then create a .env (you can create your own, or run "cp .env.example .env" to copy mine.)
Open the .env file and add your credentials. Then you're good to go.

Usage:
Run data_collection.py to fetch comments from a subreddit. This will save the fetched data as a JSON file in the data/raw directory. It will also identify and save the extreme comments (happiest, saddest, most subjective, and least subjective).
Run sentiment_analysis.py to analyze the comments.
Run historical_sentiment_analysis.py to plot historical sentiment and emotion trends. 
Finally, run visualize_sentiment.py to create visualizations of the sentiment analysis results. The script currently generates a histogram of polarity, a histogram of subjectivity, and a scatter plot of polarity vs subjectivity.
