import pandas as pd
from textblob import TextBlob

# Specify the file path
file_path = '/Users/manuyadav/Downloads/hgh.csv'
data = pd.read_csv(file_path)

# Specify the columns containing open-ended responses
open_ended_columns = [
    "Open-Ended Questions:-\n20. What do you think are the biggest advantages of EV-based delivery services?",
    "21. What concerns or challenges do you associate with EV-based deliveries?",
    "22. What additional features would make EV-based deliveries more appealing to you?"
]

# Extract the relevant columns and drop rows with NaN values
text_data = data[open_ended_columns].dropna()

# Rename columns for easier handling
text_data.columns = ["Advantages", "Challenges", "Additional Features"]

# Define a function to compute polarity and subjectivity using TextBlob
def analyze_sentiment(text):
    sentiment = TextBlob(text).sentiment
    return sentiment.polarity, sentiment.subjectivity

# Apply sentiment analysis to each column
for column in text_data.columns:
    text_data[f"{column}_Polarity"], text_data[f"{column}_Subjectivity"] = zip(
        *text_data[column].apply(lambda x: analyze_sentiment(str(x)))
    )

# Display the first few rows of the results
print(text_data.head())

# Calculate and print the average sentiment for each column
average_sentiment = text_data[[
    "Advantages_Polarity", "Challenges_Polarity", "Additional Features_Polarity"
]].mean()

print("\nAverage Sentiment Scores:")
print(average_sentiment)

# Save the results to a new CSV file
output_file = '/Users/manuyadav/Downloads/sentiment_analysis_results.csv'
text_data.to_csv(output_file, index=False)
print(f"\nSentiment analysis results saved to {output_file}")