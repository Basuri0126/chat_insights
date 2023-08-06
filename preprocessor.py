import re
import pandas as pd


def preprocessor(data):

    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{1,2}\s-\s'
    message = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    df = pd.DataFrame({'user_message': message, 'message_date': dates})

    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%Y, %H:%M - ')

    # Using the format string ensures that pandas can correctly parse the date strings and
    # convert them into datetime objects.
    # Without the format specification, pandas would use its default parsing method,
    # which may not work if the date strings are not in a recognized format.
    # Specifying the format helps avoid any ambiguity and ensures the correct conversion of dates to datetime objects.

    df.rename(columns={'message_date': 'date'}, inplace=True)

    # separate user message and user dates
    users = []
    messages = []
    for msg in df['user_message']:
        x = re.split('([\w\W]+?):\s', msg)
        if x[1:]:
            users.append(x[1])
            messages.append(x[2])
        else:
            users.append('group notification')
            messages.append(x[0])

    df['users'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    df['users'].replace('+91 74177 08734', 'Gurpreet Singh', inplace=True)
    df['users'].replace('+91 85100 24889', 'Siddhant Chhatwal', inplace=True)
    df['users'].replace('Admin', 'Kunal(DJ)', inplace=True)
    df['users'].replace('+91 87009 16851', 'Kunal(NCC)', inplace=True)
    df['users'].replace('Vivek Pandey🐾', 'Vivek Pandey', inplace=True)
    df['users'].replace('+91 99537 47073', 'Simran Arora', inplace=True)
    df['users'].replace('Rohit', 'Rohit(NCC Uttarakhand)', inplace=True)
    df['users'].replace('Rohit CVZ', 'Rohit(Sagar Friend)', inplace=True)
    df['users'].replace('+91 84487 12812', 'Rishabh Chauhan', inplace=True)
    df['users'].replace('+91 91937 22980', 'Priti Gupta', inplace=True)
    df['users'].replace('M@n!$π', 'Manish', inplace=True)
    df['users'].replace('Parnav C', 'Parnav Chutiya', inplace=True)
    df['users'].replace('Kunal Singh Cvs', 'kunal Singh', inplace=True)
    df['users'].replace('Sagar Cvs', 'Sagar Adhikari(badwa)', inplace=True)
    df['users'].replace('Harsh Cvs', 'Harsh kumar', inplace=True)
    df['users'].replace('+91 95205 76470', 'Digvijay', inplace=True)
    df['users'].replace('Nistha', 'Nistha Khurana', inplace=True)
    df['users'].replace('Maikuri', 'Priyanshu Maikuri', inplace=True)
    df['users'].replace('Adarsh Cs', 'Adarsh kumar', inplace=True)
    df['users'].replace('Khushal', 'Khushal Rastogi', inplace=True)
    df['users'].replace('Bhati', 'Dharmendra Bhati', inplace=True)
    df['users'].replace('Prachi', 'Prachi Arora', inplace=True)
    df['users'].replace('🚩Abhishek Phulera', 'Abhishek Phulera', inplace=True)
    df['users'].replace('+91 88601 80972', 'kanishk Madhukar', inplace=True)
    df['users'].replace('+91 90502 62919', '~ = (pta nhi kon hai)', inplace=True)
    df['users'].replace('+91 88604 06273', 'Umang Tayal', inplace=True)
    df['users'].replace('+91 99991 92276', 'Nitin Vinod Tanwar', inplace=True)
    df['users'].replace('mehak kataria', 'Mehak Kataria', inplace=True)

    df.drop(7616, inplace=True)

    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    df['day_name'] = df['date'].dt.day_name()
    df['month_num'] = df['date'].dt.month
    df['month_day'] = df['month'].astype(str) + '-' + df['day'].astype(str)
    df['message_count'] = df.groupby(['month_day', 'users'])['message'].transform('count')
    df['data_info'] = df['year'].astype(str) + '-' + df['month_num'].astype(str)

    period = []
    for hour in df[['day', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + '-' + str('00'))
        elif hour == 0:
            period.append(str('00') + '-' + str(hour + 1))
        else:
            period.append(str(hour) + '-' + str(hour + 1))

    df['period'] = period

    return df
