from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji


def fetch_state(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # total number of messages
    num_messages = df.shape[0]

    # total number of words
    word = []
    for message in df['message']:
        word.extend(message.split())

    # total number of media
    num_media = df[df['message'] == '<Media omitted>\n'].shape[0]

    # total number of links
    extractor = URLExtract()
    links = []
    for message in df['message']:
        links.extend(extractor.find_urls(message))
    return num_messages, len(word),num_media,len(links)

def most_busy_users(df):
    x = df['user'].value_counts().head()
    most_busy_df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(columns={'count': 'percent'})
    return x,most_busy_df

def create_wordcloud(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    df = df[df['message'] != '<Media omitted>\n']
    wc = WordCloud(background_color= 'white',width=500,height = 300,min_font_size = 10,margin = 20)
    wc_df = wc.generate(df['message'].str.cat(sep = " "))
    return wc_df

def most_common_words(selected_user,df):
    f = open('stopwords.txt','r')
    stop_words = f.read()
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    words = []
    for message in temp['message']:
        for word in message.split():
            if word not in stop_words:
                words.append(word)
    most_common_words_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_words_df

def emoji_helper(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])
    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df

def monthly_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + '-' + str(timeline['year'][i]))
    timeline['time'] = time
    return timeline

def daily_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    daily_timeline = df.groupby('only_date').count()['message'].reset_index()
    return daily_timeline

def weekly_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()

def monthly_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()

def activity_heatmap(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    return df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)
