import time
import pandas as pd
import numpy as np
import statistics as st
import json

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("\nWhich city? chicago, new york, washington. \n").lower()
        if city in ['chicago', 'new york', 'washington']:
            break
        else:
            print('Invalid input, try again!')


    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        month = input("\nWhich month? january, february, march, april, may, june, or type all to apply for all months. \n").lower()
        if month in ["january", "february", "march", "april", "may", "june", "all"]:
            break
        else:
            print('try again!')


    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("\nWhich day? monday, tuesday, wednesday, thursday, friday, saturday, sunday, or type all to apply for all days. \n").lower()
        if day in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday", "all"]:
            break
        else:
            print('try again!')



    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    file_name = CITY_DATA[city]
    df = pd.read_csv(file_name)

    df['Start Time'] = pd.to_datetime(arg = df['Start Time'], format = '%Y-%m-%d %H:%M:%S')

    if month != 'all':
        df['month'] = df['Start Time'].dt.month
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        df = df.loc[df['month'] == month]

    if day != 'all':
        df['day_of_week'] = df['Start Time'].dt.weekday_name

        df = df.loc[df['day_of_week'] == day.title()]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    df['Start Time'] = pd.to_datetime(arg = df['Start Time'], format = '%Y-%m-%d %H:%M:%S')

    month = df['Start Time'].dt.month
    weekday_name = df['Start Time'].dt.weekday_name
    hour = df['Start Time'].dt.hour

    # TO DO: display the most common month
    most_common_month = month.mode()[0]
    print('The most common month: ', most_common_month)


    # TO DO: display the most common day of week
    most_common_day_of_week = weekday_name.mode()[0]
    print('The most common day of week: ', most_common_day_of_week)


    # TO DO: display the most common start hour
    common_start_hour = hour.mode()[0]
    print('The most common start hour: ', common_start_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    most_common_start_station = st.mode(df['Start Station'])
    print('\nThe most common start station is {}\n'.format(most_common_start_station))


    # TO DO: display most commonly used end station
    most_common_end_station = st.mode(df['End Station'])
    print('\nThe most common end station is {}\n'.format(most_common_end_station))


    # TO DO: display most frequent combination of start station and end station trip
    df['Start End'] = df['Start Station'].map(str) + ' to ' + df['End Station']
    popular_start_end = df['Start End'].value_counts().idxmax()
    print('The most frequent combination of start station and end station: ',popular_start_end)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    Total_Travel_Time = sum(df['Trip Duration'])
    print('\nTotal travel time:', Total_Travel_Time/86400, " Days")



    # TO DO: display mean travel time
    Mean_Travel_Time = df['Trip Duration'].mean()
    print('\nMean travel time:', Mean_Travel_Time/60, " Minutes")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    no_of_subscribers = df['User Type'].str.count('Subscriber').sum()
    no_of_customers = df['User Type'].str.count('Customer').sum()
    print('\nNumber of subscribers are {}\n'.format(int(no_of_subscribers)))
    print('\nNumber of customers are {}\n'.format(int(no_of_customers)))


    # TO DO: Display counts of gender
    if('Gender' in df):
        male_count = df['Gender'].str.count('Male').sum()
        female_count = df['Gender'].str.count('Female').sum()
        print('\nNumber of male users are {}\n'.format(int(male_count)))
        print('\nNumber of female users are {}\n'.format(int(female_count)))


    # TO DO: Display earliest, most recent, and most common year of birth
    if('Birth Year' in df):
        earliest_birthday = df['Birth Year'].min()
        recent_birthday = df['Birth Year'].max()
        most_common_birthday = st.mode(df['Birth Year'])
        print('\nEarliest year of birth is {}\n'.format(int(earliest_birthday)))
        print('\nRecent year of birth is {}\n'.format(int(recent_birthday)))
        print('\nMost common year of birth is {}\n'.format(int(most_common_birthday)))



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):

    row_length = df.shape[0]

    for i in range(0, row_length, 5):

        yes = input('\nDo you want to see the raw data of user trip? Type Yes or No\n ')
        if yes.lower() != 'yes':
            break

        row_data = df.iloc[i: i + 5].to_json(orient='records', lines=True).split('\n')
        for row in row_data:
            parsed_row = json.loads(row)
            json_row = json.dumps(parsed_row, indent=2)
            print(json_row)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
