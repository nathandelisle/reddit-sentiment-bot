import os
import json
import matplotlib.pyplot as plt

def load_data(input_filename):
    with open(input_filename, 'r') as f:
        data = json.load(f)
    return data

def plot_histogram(data, field, title, xlabel, ylabel, output_filename):
    values = [comment[field] for comment in data]
    plt.hist(values, bins=20, edgecolor='black')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True)
    os.makedirs(os.path.dirname(output_filename), exist_ok=True)
    plt.savefig(output_filename)
    plt.clf()

def plot_scatter(data, x_field, y_field, title, xlabel, ylabel, output_filename):
    x_values = [comment[x_field] for comment in data]
    y_values = [comment[y_field] for comment in data]
    plt.scatter(x_values, y_values, alpha=0.5)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True)
    os.makedirs(os.path.dirname(output_filename), exist_ok=True)
    plt.savefig(output_filename)
    plt.clf()

def main():
    input_filename = input("Enter the filename of the sentiment analysis results (e.g., data/processed/reddit_sentiment_python_2024-08-06_to_2024-08-07.json): ")

    data = load_data(input_filename)

    plot_histogram(data, 'polarity', 'Histogram of Polarity', 'Polarity', 'Frequency', 'data/plots/polarity_histogram.png')
    plot_histogram(data, 'subjectivity', 'Histogram of Subjectivity', 'Subjectivity', 'Frequency', 'data/plots/subjectivity_histogram.png')
    plot_scatter(data, 'polarity', 'subjectivity', 'Polarity vs Subjectivity', 'Polarity', 'Subjectivity', 'data/plots/polarity_vs_subjectivity.png')

    print("Visualizations completed and saved to the 'data/plots' directory.")

if __name__ == "__main__":
    main()
