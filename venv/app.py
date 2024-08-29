import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
import numpy as np

st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    st.dataframe(df)

    #fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.sort()
    user_list.insert(0,"Overall")

    selected_user = st.sidebar.selectbox("show analysis with respect to",user_list)

    if st.sidebar.button("Show Analysis"):

        num_messages, words, num_images, num_links = helper.fetch_stats(selected_user,df)

        col1,col2,col3,col4 = st.columns(4)

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
        
        # finding the busiest user in group level(in group)
        if selected_user == 'Overall':
            st.title('Most Active Users')
            x,new_df = helper.most_active_users(df)
            fig, ax = plt.subplots()

            col1,col2 = st.columns(2)

            with col1:
                ax.bar(x.index,x.values,color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)
        
        #wordcloud
        st.title("WordCloud")
        df_wc = helper.create_wordcloud(selected_user,df)
        fig,ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)
        
        #most common words
        most_common_df = helper.most_common_words(selected_user,df)

        fig,ax = plt.subplots()
        ax.barh(most_common_df[0],most_common_df[1])
        plt.xticks(rotation='vertical')
        st.title('Most Common Words')
        st.pyplot(fig)

        # emoji analysis
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
        monthly_timeline, daily_timeline = helper.timeline_analysis(selected_user,df)

        # Plot the timelines
        fig1, fig2 = helper.plot_timeline(monthly_timeline, daily_timeline)

        # Display the Monthly Timeline
        st.header("Monthly Timeline")
        st.pyplot(fig1)

        # Display the Daily Timeline
        st.header("Daily Timeline")
        st.pyplot(fig2)













        







