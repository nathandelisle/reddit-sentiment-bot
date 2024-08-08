import os
import json
import pandas as pd
import matplotlib.pyplot as plt

def load_data(input_filename):
    with open(input_filename, 'r') as f:
        data = json.load(f)
    return data

def prepare_time_series(data):
    records = []
    for comment in data:
        created_utc = pd.to_datetime(comment['created_utc'], unit='s')
        polarity = comment['polarity']
        subjectivity = comment['subjectivity']
        emotion_label = comment['emotion_label']
        records.append((created_utc, polarity, subjectivity, emotion_label))
    
    df = pd.DataFrame(records, columns=['created_utc', 'polarity', 'subjectivity', 'emotion_label'])
    df.set_index('created_utc', inplace=True)
    return df

def plot_time_series(df, field, title, ylabel, output_filename):
    df_numeric = df[[field]]  # Select only the numeric column for resampling
    df_resampled = df_numeric.resample('D').mean()  # Resample by day and calculate mean
    plt.plot(df_resampled.index, df_resampled[field], marker='o')
    plt.title(title)
    plt.xlabel('Date')
    plt.ylabel(ylabel)
    plt.grid(True)
    os.makedirs(os.path.dirname(output_filename), exist_ok=True)
    plt.savefig(output_filename)
    plt.clf()

def plot_emotion_trends(df, output_filename):
    emotion_counts = df.groupby([pd.Grouper(freq='D'), 'emotion_label']).size().unstack(fill_value=0)
    emotion_counts.plot(kind='line', marker='o')
    plt.title('Historical Emotion Trend')
    plt.xlabel('Date')
    plt.ylabel('Count')
    plt.grid(True)
    os.makedirs(os.path.dirname(output_filename), exist_ok=True)
    plt.savefig(output_filename)
    plt.clf()

def main():
    input_filename = input("Enter the filename of the sentiment analysis results (e.g., data/processed/reddit_sentiment_python_2024-08-06_to_2024-08-07.json): ")

    data = load_data(input_filename)
    df = prepare_time_series(data)

    plot_time_series(df, 'polarity', 'Historical Polarity Trend', 'Average Polarity', 'data/plots/historical_polarity_trend.png')
    plot_time_series(df, 'subjectivity', 'Historical Subjectivity Trend', 'Average Subjectivity', 'data/plots/historical_subjectivity_trend.png')
    plot_emotion_trends(df, 'data/plots/historical_emotion_trend.png')

    print("Historical sentiment and emotion trend analysis completed and saved to the 'data/plots' directory.")

if __name__ == "__main__":
    main()
