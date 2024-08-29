from urlextract import URLExtract
from wordcloud import  WordCloud
from collections import Counter
import matplotlib.pyplot as plt
import pandas as pd
import emoji
from textblob import TextBlob
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import os



extract = URLExtract()
def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    #fetch no of words
    num_messages = df.shape[0]
    words = []
    for message in df['message']:
            words.extend(message.split())
    #fetch no of images
    num_images = df[df['message']=='image omitted\n'].shape[0]

    #fetch no of links shared
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))

    return num_messages, len(words), num_images,len(links)

def most_active_users(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'user':'name','count':'percent'})
    return x ,df

def create_wordcloud(selected_user,df):
  
    f = open('stopwords-T-H-E.txt','r')
    stop_words = f.read()
    
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    filtered_df = df[~df['message'].str.contains('audio omitted\n|video omitted\n|sticker omitted\n|document omitted\n$|omitted\n$')] 

    def remove_stop_words(message):
        y =[]
        for  word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return  " ".join(y)
                 

    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    filtered_df['message'] = filtered_df['message'].apply(remove_stop_words)
    df_wc = wc.generate(filtered_df['message'].str.cat(sep=" "))
    return df_wc

def most_common_words(selected_user,df):
    f = open('stopwords-T-H-E.txt','r')
    stop_words = f.read()
    
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    filtered_df = df[~df['message'].str.contains('audio omitted\n|video omitted\n|sticker omitted\n|document omitted\n$|omitted\n$')]

    words = []
    for msg in filtered_df['message']:
        for word in msg.lower().split():
            if word not in stop_words:
                words.append(word)
    
    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

def emoji_helper(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df

def timeline_analysis(selected_user,df):
    # Convert 'date' to datetime format if not already done
    df['date'] = pd.to_datetime(df['date'], format='%d/%m/%y %I:%M:%S %p')

    # Create 'month_year' and 'day' columns for analysis
    df['month_year'] = df['date'].dt.to_period('M')
    df['day'] = df['date'].dt.date

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Group by month_year to analyze monthly trends
    monthly_timeline = df.groupby('month_year').count()['message'].reset_index()

    # Group by day to analyze daily trends
    daily_timeline = df.groupby('day').count()['message'].reset_index()

    return monthly_timeline, daily_timeline

def plot_timeline(monthly_timeline, daily_timeline):
    # Plotting the Monthly Timeline
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    ax1.plot(monthly_timeline['month_year'].astype(str), monthly_timeline['message'], marker='o', color='skyblue')
    ax1.set_title('Monthly Timeline of Messages')
    ax1.set_xlabel('Month-Year')
    ax1.set_ylabel('Number of Messages')
    ax1.grid(True)
    plt.xticks(rotation=90)

    # Plotting the Daily Timeline
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    ax2.plot(daily_timeline['day'], daily_timeline['message'], marker='o', color='orange')
    ax2.set_title('Daily Timeline of Messages')
    ax2.set_xlabel('Day')
    ax2.set_ylabel('Number of Messages')
    ax2.grid(True)
    plt.xticks(rotation=90)

    return fig1, fig2

def conversation_starters(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Identify the first message of each conversation
    first_messages = df[df['message'].str.contains('Hi|Hello|Hey|hii|heyy|dei|deii|oii', case=False, na=False)]  # Adjust this regex as needed

    # Count messages started by each user
    starter_counts = first_messages['user'].value_counts().reset_index()
    starter_counts.columns = ['user', 'starter_count']

    return starter_counts

def response_time(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Convert 'date' column to datetime if not already done
    df['date'] = pd.to_datetime(df['date'], format='%d/%m/%y %I:%M:%S %p')

    # Sort by date to calculate response times in order
    df = df.sort_values(by='date')

    # Calculate time differences
    df['response_time'] = df['date'].diff().dt.total_seconds() / 60  # Convert to minutes

    # Remove the first message of each user or messages without response time
    df = df.dropna(subset=['response_time'])

    # Calculate average response time
    avg_response_time = df['response_time'].mean()

    return avg_response_time

def sentiment_analysis(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Convert 'date' column to datetime if not already done
    df['date'] = pd.to_datetime(df['date'], format='%d/%m/%y %I:%M:%S %p')

    # Define a function to get sentiment
    def get_sentiment(text):
        analysis = TextBlob(text)
        if analysis.sentiment.polarity > 0:
            return 'Positive'
        elif analysis.sentiment.polarity < 0:
            return 'Negative'
        else:
            return 'Neutral'

    # Apply sentiment analysis
    df['sentiment'] = df['message'].apply(get_sentiment)

    # Calculate sentiment distribution
    sentiment_counts = df['sentiment'].value_counts()

    return sentiment_counts







    




    
 


















