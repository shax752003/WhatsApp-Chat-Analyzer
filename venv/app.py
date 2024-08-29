import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
import numpy as np
from streamlit_lottie import st_lottie
import requests
from PIL import Image
from streamlit_option_menu import option_menu

# Setting page configuration
st.set_page_config(page_title="WhatsApp Chat Analyzer", layout="wide")

# Function to access Lottie files
def lottie_url(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_code = lottie_url("https://assets10.lottiefiles.com/packages/lf20_iv4dsx3q.json")
lottie1_code = lottie_url("https://assets2.lottiefiles.com/private_files/lf30_wyrwqyr9.json")
lottie2_code = lottie_url("https://assets6.lottiefiles.com/packages/lf20_ryosrokc.json")

@st.cache(allow_output_mutation=True)
def ob():
    pass

# Apply WhatsApp theme
def apply_whatsapp_theme():
    st.markdown(
        """
        <style>
        .reportview-container {
            background-color: #ffffff;  /* White background */
        }
        .sidebar .sidebar-content {
            background-color: #25D366;  /* WhatsApp Green */
        }
        .sidebar .sidebar-content h1, .sidebar .sidebar-content h2, .sidebar .sidebar-content h3,
        .sidebar .sidebar-content p, .sidebar .sidebar-content a {
            color: #ffffff;  /* White text */
        }
        .main .block-container {
            background-color: #0E1117;  /* Light gray */
        }
        .main .block-container h1, .main .block-container h2, .main .block-container h3,
        .main .block-container p, .main .block-container a {
            color: #ffffff;  /* Black text */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# Apply the WhatsApp theme
apply_whatsapp_theme()

# Making the option menu at the sidebar
with st.sidebar:
    selected = option_menu('WhatsApp Chat Analysis',
                           ['Home', 'WhatsApp Chat Analyzer', 'Contact Us'],
                           icons=['house', 'whatsapp', 'cast'], default_index=0)

# Making the home page    
if selected == "Home":
    st.title("WhatsApp Chat Analyzer")

    # Writing the content like description, key points on the home page
    st.write("---")
    st.header("Description: WhatsApp Chat Analyzer using Machine Learning and NLP")
    st.write(''' 
The WhatsApp Chat Analyzer is a project that leverages machine learning and natural language processing techniques to analyze chat data from WhatsApp conversations. By applying advanced algorithms, the project aims to extract meaningful insights from the chat data, enabling users to gain valuable information and understand various aspects of the conversation.''')

    with st.container():
        st.write("---")
        st.header("Key Features:")
        left_column, right_column = st.columns(2)
        with left_column:
            st.write('''
            MESSAGE STATISTICS:  Analyze total message counts, word counts, images and links shared.
                     
            USER ACTIVITY:  Identify the most active users and understand communication patterns.
                     
            WORDCLOUD & COMMON WORDS:  Visualize frequently used words and generate word clouds.
                     
            EMOJI ANALYSIS:  Explore the most commonly used emojis and their frequency.
                     
            TIMELINE ANALYSIS:  Examine chat activity over time with monthly and daily timelines.
                     
            CONVERSATION STARTERS:  Discover who starts conversations the most in your chats.
                     
            RESPONSE TIME ANALYSIS:  Measure the average response time for each participant.
                     
            SENTIMENT ANALYSIS:  Analyze the sentiment of the conversations to understand the overall mood.
            ''')
        with right_column:
            st_lottie(lottie_code, height=350, key="code")

    with st.container():
        st.write("---")
        st.header("Potential Use Cases:")
        left_column, right_column = st.columns(2)
        with left_column:
            st_lottie(lottie2_code, height=300, key="android")
        with right_column:
            st.write('''
            Sentiment Analysis: Analyzing the overall sentiment of the chat to identify positive, negative, or neutral tones throughout the conversation.
            Topic Modeling: Identifying the main topics discussed in the chat and visualizing their distribution.
            User Interaction Analysis: Examining the frequency and patterns of communication between different participants.
            Keyword Extraction: Identifying frequently used keywords or phrases in the chat.
            Trend Analysis: Analyzing chat activity over time to detect spikes, lulls, or other patterns.
            ''')
        st.write("By employing machine learning and NLP techniques, the WhatsApp Chat Analyzer project enables users to gain a deeper understanding of their chat data, facilitating data-driven decision-making, sentiment monitoring, trend analysis, and other valuable insights from WhatsApp conversations.")
        st.write("---")
        st.write(''' Designed and Developed by shax752003.''')
        st.markdown('''<nav class="navbar">
        <ul style="margin: 3px; padding-left: 250px;">
            <li style="float: left; list-style: none; border-radius: 8px; margin: 20px; padding: 20px; font-family: 'Open Sans', sans-serif; color: rgb(255, 255, 255); width: 150px; text-align: center; font-size: 10px;">Privacy Policy</li>
            <li style="float: left; list-style: none; border-radius: 8px; margin: 20px; padding: 20px; font-family: 'Open Sans', sans-serif; color: rgb(255, 255, 255); width: 150px; text-align: center; font-size: 10px;">Terms and Conditions</li>
            <li style="float: left; list-style: none; border-radius: 8px; margin: 20px; padding: 20px; font-family: 'Open Sans', sans-serif; color: rgb(255, 255, 255); width: 150px; text-align: center; font-size: 10px;">Copyright</li>
        </ul>
    </nav>''', unsafe_allow_html=True)

# Sidebar content
st.sidebar.title("WhatsApp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    st.dataframe(df)

    # Fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Show analysis with respect to", user_list)

    if st.sidebar.button("Show Analysis"):
        num_messages, words, num_images, num_links = helper.fetch_stats(selected_user, df)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Images Shared")
            st.title(num_images)
        with col4:
            st.header("Links Shared")
            st.title(num_links)
        
        # Finding the busiest user in group level (in group)
        if selected_user == 'Overall':
            st.title('Most Active Users')
            x, new_df = helper.most_active_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values, color='#25D366')  # WhatsApp Green
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)
        
        # Wordcloud
        st.title("WordCloud")
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)
        
        # Most common words
        most_common_df = helper.most_common_words(selected_user, df)

        fig, ax = plt.subplots()
        ax.barh(most_common_df[0], most_common_df[1])
        plt.xticks(rotation='vertical')
        st.title('Most Common Words')
        st.pyplot(fig)

        # Emoji analysis
        emoji_df = helper.emoji_helper(selected_user, df)
        st.title("Emoji Analysis")

        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors)
            ax.set_title('Top 5 Emojis Used')
            st.pyplot(fig)
        
        # Timeline Analysis
        st.title("Timeline Analysis")

        # Get timeline data from helper
        monthly_timeline, daily_timeline = helper.timeline_analysis(selected_user, df)

        # Plot the timelines
        fig1, fig2 = helper.plot_timeline(monthly_timeline, daily_timeline)

        # Display the Monthly Timeline
        st.header("Monthly Timeline")
        st.pyplot(fig1)

        # Display the Daily Timeline
        st.header("Daily Timeline")
        st.pyplot(fig2)

        # Conversation Starters
        st.title("Conversation Starters")
        starter_df = helper.conversation_starters(selected_user, df)

        if not starter_df.empty:
            fig, ax = plt.subplots()
            ax.bar(starter_df['user'], starter_df['starter_count'], color='purple')
            ax.set_xlabel('User')
            ax.set_ylabel('Number of Conversations Started')
            ax.set_title('Top Conversation Starters')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        else:
            st.write("No conversation starters found.")

        # Response Time Analysis
        st.title("Response Time")
        avg_response_time = helper.response_time(selected_user, df)

        st.write(f"The average response time for {selected_user} is {avg_response_time:.2f} minutes.")

        # Sentiment Analysis
        st.title("Sentiment Analysis")
        sentiment_counts = helper.sentiment_analysis(selected_user, df)

        fig, ax = plt.subplots()
        ax.pie(sentiment_counts, labels=sentiment_counts.index, autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors)
        ax.set_title('Sentiment Distribution')
        st.pyplot(fig)
