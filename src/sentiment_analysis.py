import os
import json
from textblob import TextBlob
from transformers import pipeline

def analyze_sentiment(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity, blob.sentiment.subjectivity

def classify_emotion(text, classifier):
    max_length = 512
    truncated_text = text[:max_length]
    return classifier(truncated_text)[0]

def process_comments(comments, classifier):
    results = []
    for comment in comments:
        polarity, subjectivity = analyze_sentiment(comment['body'])
        emotion = classify_emotion(comment['body'], classifier)
        comment['polarity'] = polarity
        comment['subjectivity'] = subjectivity
        comment['emotion_label'] = emotion['label']
        comment['emotion_score'] = emotion['score']
        results.append(comment)
    return results

def save_results(data, output_filename):
    os.makedirs(os.path.dirname(output_filename), exist_ok=True)
    with open(output_filename, 'w') as f:
        json.dump(data, f, indent=4)

def find_extreme_comments(comments):
    happiest_comment = max(comments, key=lambda x: x['polarity'])
    saddest_comment = min(comments, key=lambda x: x['polarity'])
    most_subjective_comment = max(comments, key=lambda x: x['subjectivity'])
    least_subjective_comment = min(comments, key=lambda x: x['subjectivity'])
    
    return {
        "happiest_comment": happiest_comment,
        "saddest_comment": saddest_comment,
        "most_subjective_comment": most_subjective_comment,
        "least_subjective_comment": least_subjective_comment
    }

def main():
    input_filename = input("Enter the filename of the comments data (e.g., data/raw/reddit_data_lostafriend_2024-08-01_to_2024-08-05.json): ")
    output_filename = input("Enter the filename to save the sentiment analysis results (e.g., data/processed/reddit_sentiment_lostafriend_2024-08-06_to_2024-08-07.json): ")
    extreme_comments_filename = input("Enter the filename to save the extreme comments (e.g., data/processed/extreme_comments_lostafriend_2024-08-06_to_2024-08-07.json): ")

    with open(input_filename, 'r') as f:
        comments = json.load(f)
    
    classifier = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", return_all_scores=False)
    processed_comments = process_comments(comments, classifier)
    
    save_results(processed_comments, output_filename)
    extreme_comments = find_extreme_comments(processed_comments)
    save_results(extreme_comments, extreme_comments_filename)

    print(f"Sentiment and emotion analysis completed and saved to {output_filename}")
    print(f"Extreme comments saved to {extreme_comments_filename}")

if __name__ == "__main__":
    main()
