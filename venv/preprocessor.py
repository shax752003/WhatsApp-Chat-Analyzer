
import re
import pandas as pd
import calendar

def preprocess(data):
    # Define the regex pattern to split messages and extract dates
    pattern = r'\[\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}:\d{2}\s[APM]{2}\]'
    messages = re.split(pattern, data)[1:] 
    dates = re.findall(pattern, data)
    dates = [date.replace('\u202f', ' ').strip('[]') for date in dates]

    # Create DataFrame
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})

    # Convert the 'message_date' column to datetime format
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %I:%M:%S %p')

    # Rename the 'message_date' column to 'date'
    df.rename(columns={'message_date': 'date'}, inplace=True)

    # Format the 'date' column to display in AM/PM format
    df['date'] = df['date'].dt.strftime('%d/%m/%y %I:%M:%S %p')

    # Separate users and messages
    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split(r'([\w\W]+?):\s', message)
        if len(entry) > 2:  # Check if there's a user and message
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])
    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    # Convert the 'date' column to datetime format
    df['datetime'] = pd.to_datetime(df['date'], format='%d/%m/%y %I:%M:%S %p')

    # Create new columns for year, month, day, and hour
    df['year'] = df['datetime'].dt.year
    df['month'] = df['datetime'].dt.month
    df['day'] = df['datetime'].dt.day
    df['hour'] = df['datetime'].dt.hour

    # Drop the 'datetime' column if you don't need it anymore
    df.drop(columns=['datetime'], inplace=True)
    
    # Drop the row at index 0 if necessary
    df.drop(index=0, inplace=True, errors='ignore')

    # Reset the index to keep it continuous
    df.reset_index(drop=True, inplace=True)
    
    # Convert the 'month' column from numbers to month names
    df['month'] = df['month'].apply(lambda x: calendar.month_name[x])
    
    # Add placeholder labels for message classification
    df['label'] = 'Other'  # Placeholder, modify according to your label needs
    
    return df

