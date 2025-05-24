import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title="WhatsApp Chat Analyzer",
    page_icon="💬",
    layout="wide"
)

st.sidebar.title('Whatsapp Chat Analyzer')
file_uploader = st.sidebar.file_uploader('Choose a file',format('txt'))

if file_uploader is not None:
    bytes_data = file_uploader.getvalue()
    data = bytes_data.decode('utf-8')
    df = preprocessor.preprocess(data)

    # fetch unique users

    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,'Overall')

    selected_user = st.sidebar.selectbox('Show analysis for:',user_list)

    if st.sidebar.button('Show Analysis'):
        st.title(f'Chat Analysis: {selected_user}')
        st.header('📊 Basic Statistics')
        col1,col2,col3,col4 = st.columns(4)
        num_messages,num_words,num_media,num_links = helper.fetch_state(selected_user, df)
        with col1:
            st.metric('Total Messages', num_messages)
        with col2:
            st.metric('Total Words', num_words)
        with col3:
            st.metric('Media Shared', num_media)
        with col4:
            st.metric('Links Shared', num_links)

        # timeline
        st.header('📅 Timelines')
        st.subheader('Monthly Timeline')
        timeline = helper.monthly_timeline(selected_user, df)
        timeline.set_index('time',inplace = True)
        st.line_chart(timeline['message'])

        # daily timeline
        st.subheader('Daily Timeline')
        daily_timeline = helper.daily_timeline(selected_user,df)
        daily_timeline.set_index('only_date',inplace = True)
        st.line_chart(daily_timeline['message'])

        # activity map

        st.header('🕒 Activity Patterns')
        col1,col2 = st.columns(2)
        with col1:
            st.subheader('Most Active Day')
            busy_day = helper.weekly_activity_map(selected_user, df)
            st.bar_chart(busy_day)

        with col2:
            st.subheader('Most Active Month')
            busy_month = helper.monthly_activity_map(selected_user, df)
            st.bar_chart(busy_month)


        # activity heatmap
        st.subheader('Activity Heatmap')
        activity_heatmap = helper.activity_heatmap(selected_user, df)
        fig,ax = plt.subplots()
        ax = sns.heatmap(activity_heatmap)
        st.pyplot(fig)
        # finding the busiest user in the group (group level analysis)
        st.header('👥 Most Active Users')
        x,most_busy_df = helper.most_busy_users(df)
        col1,col2 = st.columns(2)
        with col1:
            st.subheader('Top Users by Message Count')
            st.bar_chart(x)

        with col2:
            st.subheader('User Participation')
            st.dataframe(most_busy_df)
        # word analysis
        st.header('📝 Word Analysis')
        # wordcloud
        st.subheader('Word Cloud')
        wc_df = helper.create_wordcloud(selected_user,df)
        fig,ax = plt.subplots()
        ax.imshow(wc_df)
        st.pyplot(fig)

        # most common words
        st.subheader('Most Common Words')
        most_common_words_df = helper.most_common_words(selected_user, df)
        most_common_words_df.rename(columns = {0:'word',1:'frequency'},inplace=True)
        most_common_words_df.set_index('word',inplace=True)
        st.bar_chart(most_common_words_df)

        # emoji analysis

        emoji_df = helper.emoji_helper(selected_user, df)
        emoji_df.rename(columns = {0:'emoji',1:'frequency'},inplace = True)
        st.header('😃 Emoji Analysis')
        col1,col2 = st.columns(2)
        with col1:
            st.subheader('Top Emojis')
            st.dataframe(emoji_df)
        with col2:
            st.subheader('Emoji Frequency')
            emoji_df.set_index('emoji',inplace = True)
            st.bar_chart(emoji_df)
