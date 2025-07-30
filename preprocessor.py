import re
import pandas as pd

def preprocess(data):
    # Clean special unicode chars like \u202f (narrow no-break space)
    data = data.replace('\u202f', ' ').replace('\u200e', '')

    # Pattern to match date and time (handles both 12-hour format and optional seconds)
    pattern = r'\[\d{2}/\d{2}/\d{2},\s\d{1,2}:\d{2}(?::\d{2})?\s?(?:AM|PM|am|pm)?\]'

    # Split data by pattern (ignoring the first entry, which is always empty)
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    df = pd.DataFrame({'user_message': messages, 'message_date': dates})
    df['message_date'] = df['message_date'].str.strip("[]")

    # Try parsing datetime with 12-hour format first
    try:
        df['message_date'] = pd.to_datetime(df['message_date'], format="%d/%m/%y, %I:%M:%S %p")
    except:
        # If failed, parse with 24-hour format
        try:
            df['message_date'] = pd.to_datetime(df['message_date'], format="%d/%m/%y, %H:%M:%S")
        except:
            # If failed, fallback to 24-hour format without seconds
            df['message_date'] = pd.to_datetime(df['message_date'], format="%d/%m/%y, %H:%M")

    df.rename(columns={'message_date': 'date'}, inplace=True)

    users = []
    messages = []

    for message in df['user_message']:
        # Split the message if it contains a user prefix, otherwise treat it as a personal chat
        entry = re.split(r'([\w\W]+?):\s', message, maxsplit=1)

        if len(entry) == 3:  # Group chat
            users.append(entry[1].strip())  # Strip leading/trailing spaces from user
            cleaned_message = entry[2].strip().replace('\n', ' ').replace('"', '')
            messages.append(cleaned_message)
        else:  # Personal chat (no user name prefix)
            users.append('Personal Chat')  # Or you can assign a specific name
            cleaned_message = entry[0].strip().replace('\n', ' ').replace('"', '')
            messages.append(cleaned_message)

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    # Extract date-related information for analysis
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    return df
