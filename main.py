#!pip install emoji
#!pip install vaderSentiment
'''from googleapiclient.discovery import build
import re
import emoji
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
import pandas as pd

API_KEY = 'AIzaSyAh31utKnlakU844PaRrGAXv7FTFrZsmdg'
 
youtube = build('youtube', 'v3', developerKey=API_KEY) 
# Taking input from the user 
video_id = input('Enter Youtube Video URL: ')[-11:]
print("video id: " + video_id)
 

video_response = youtube.videos().list(
    part='snippet',
    id=video_id
).execute()
 
# Splitting the response
video_snippet = video_response['items'][0]['snippet']
uploader_channel_id = video_snippet['channelId']
print("channel id: " + uploader_channel_id)

print("Fetching Comments...")
comments = []
nextPageToken = None
while len(comments) < 600:
    request = youtube.commentThreads().list(
        part='snippet',
        videoId=video_id,
        maxResults=100,  
        pageToken=nextPageToken
    )
    response = request.execute()
    for item in response['items']:
        comment = item['snippet']['topLevelComment']['snippet']
        
        if comment['authorChannelId']['value'] != uploader_channel_id:
            comments.append(comment['textDisplay'])
    nextPageToken = response.get('nextPageToken')
 
    if not nextPageToken:
        break
# Print the 5 comments
comments[:5]

hyperlink_pattern = re.compile(
    r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
 
threshold_ratio = 0.65
 
relevant_comments = []
 
# Inside your loop that processes comments
for comment_text in comments:
 
    comment_text = comment_text.lower().strip()
 
    emojis = emoji.emoji_count(comment_text)
 
    # Count text characters (excluding spaces)
    text_characters = len(re.sub(r'\s', '', comment_text))
 
    if (any(char.isalnum() for char in comment_text)) and not hyperlink_pattern.search(comment_text):
        if emojis == 0 or (text_characters / (text_characters + emojis)) > threshold_ratio:
            relevant_comments.append(comment_text)
 
# Print the relevant comments
relevant_comments[:10]

f = open("ytcomments.txt", 'w', encoding='utf-8')
for idx, comment in enumerate(relevant_comments):
    f.write(str(comment)+"\n")
f.close()
print("Comments stored successfully!")

def sentiment_scores(comment, polarity):

  # Creating a SentimentIntensityAnalyzer object.
  sentiment_object = SentimentIntensityAnalyzer()

  sentiment_dict = sentiment_object.polarity_scores(comment)
  polarity.append(sentiment_dict['compound'])
  print(sentiment_dict)

  return polarity


polarity = []
positive_comments = []
negative_comments = []
neutral_comments = []

f = open("ytcomments.txt", 'r', encoding='`utf-8')
print("Reading Comments...")
comments = f.readlines()
f.close()
print("Analysing Comments...")
for index, items in enumerate(comments):
    polarity = sentiment_scores(items, polarity)


    if polarity[-1] > 0.05:
        positive_comments.append(items)
    elif polarity[-1] < -0.05:
        negative_comments.append(items)
    else:
        neutral_comments.append(items)

print(polarity)

avg_polarity = sum(polarity)/len(polarity)
print("Average Polarity:", avg_polarity)
if avg_polarity>0.05:
    print("The Video has got a Positive response")
elif avg_polarity<-0.05:
    print("The Video has got a Negative response")
else:
    print("The Video has got a Neutral response")

print("The comment with most positive sentiment:", comments[polarity.index(max(polarity))], "with score", max(polarity), "and length", len(comments[polarity.index(max(polarity))]))
print("The comment with most negative sentiment:", comments[polarity.index(min(polarity))], "with score", min(polarity), "and length", len(comments[polarity.index(min(polarity))]))


positive_count = len(positive_comments)
negative_count = len(negative_comments)
neutral_count = len(neutral_comments)

# labels and data for Bar chart
labels = ['Positive', 'Negative', 'Neutral']
comment_counts = [positive_count, negative_count, neutral_count]

# Creating bar chart
plt.bar(labels, comment_counts, color=['blue', 'red', 'grey'])

# Adding labels and title to the plot
plt.xlabel('Sentiment')
plt.ylabel('Comment Count')
plt.title('Sentiment Analysis of Comments')

# Displaying the chart
plt.show()

# labels and data for Bar chart
labels = ['Positive', 'Negative', 'Neutral']
comment_counts = [positive_count, negative_count, neutral_count]

plt.figure(figsize=(10, 6)) # setting size

# plotting pie chart
plt.pie(comment_counts, labels=labels)

# Displaying Pie Chart
plt.show()'''


# main.py
import sys
from googleapiclient.discovery import build
import re
import emoji
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
import pandas as pd

def fetch_comments(video_id):
    # Function to fetch comments based on video ID
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    comments = []
    nextPageToken = None
    while len(comments) < 600:
        request = youtube.commentThreads().list(
            part='snippet',
            videoId=video_id,
            maxResults=100,
            pageToken=nextPageToken
        )
        response = request.execute()
        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']
            comments.append(comment['textDisplay'])
        nextPageToken = response.get('nextPageToken')
        if not nextPageToken:
            break
    return comments

def analyze_sentiment(comments):
    # Function to perform sentiment analysis
    relevant_comments = []
    for comment_text in comments:
        comment_text = comment_text.lower().strip()
        emojis = emoji.emoji_count(comment_text)
        text_characters = len(re.sub(r'\s', '', comment_text))
        if emojis == 0 or (text_characters / (text_characters + emojis)) > 0.65:
            relevant_comments.append(comment_text)
    
    analyzer = SentimentIntensityAnalyzer()
    polarity = [analyzer.polarity_scores(comment)['compound'] for comment in relevant_comments]
    return polarity

def plot_sentiment_analysis(polarity):
    # Function to plot sentiment analysis results
    positive_count = sum(1 for p in polarity if p > 0.05)
    negative_count = sum(1 for p in polarity if p < -0.05)
    neutral_count = len(polarity) - positive_count - negative_count

    labels = ['Positive', 'Negative', 'Neutral']
    comment_counts = [positive_count, negative_count, neutral_count]

    # Creating bar chart
    plt.figure(figsize=(8, 6))
    plt.bar(labels, comment_counts, color=['blue', 'red', 'grey'])
    plt.xlabel('Sentiment')
    plt.ylabel('Comment Count')
    plt.title('Sentiment Analysis of Comments')
    plt.savefig('templates/histogram.png')

    # Creating pie chart
    plt.figure(figsize=(8, 6))
    plt.pie(comment_counts, labels=labels, autopct='%1.1f%%', colors=['green', 'red', 'grey'])
    plt.title('Sentiment Distribution')
    # Save the pie chart image in the templates folder
    plt.savefig('templates/pie_chart.png')


def main(youtube_url):
    
    # Extract video ID from YouTube URL
    video_id = youtube_url[-11:]
    
    print("video id: " + video_id)
    # Fetch comments based on video ID
    comments = fetch_comments(video_id)

    # Analyze sentiment of comments
    sentiment_results = analyze_sentiment(comments)

    # Plot sentiment analysis results
    plot_sentiment_analysis(sentiment_results)

if __name__ == "__main__":
    API_KEY = 'AIzaSyAh31utKnlakU844PaRrGAXv7FTFrZsmdg'
    youtube_url = "https://www.youtube.com/watch?v=XBdJk8OfGqg"
    #youtube_url = sys.argv[1]
    main(youtube_url)
