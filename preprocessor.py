import re
import pandas as pd
import unicodedata
def preprocess(data):
    pattern = r'\d{1,2}/\d{1,2}/\d{1,2},\s\d{1,2}:\d{1,2}\s(?:AM|PM)\s-\s'
    clean_data = unicodedata.normalize('NFKC', data)
    messages = re.split(pattern, clean_data)[1:]
    dates = re.findall(pattern, clean_data)
    df = pd.DataFrame({'user_message': messages, 'date': dates})
    df['date'] = pd.to_datetime(df['date'], format='%m/%d/%y, %I:%M %p - ', errors='raise')

    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split(r'([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns='user_message', inplace=True)

    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['month_num'] = df['date'].dt.month
    df['only_date'] = df['date'].dt.date
    df['day_name'] = df['date'].dt.day_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    period = []
    for hour in df['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))
    df['period'] = period

    return df
