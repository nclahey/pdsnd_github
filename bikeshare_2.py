import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
weekdays = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('Which city would you like to look at? (Chicago, New York City, or Washington): ').strip().lower()

    # get user input for month (all, january, february, ... , june)
    month = input('What month do you want to filter by? (January, February, March, etc... or "all"): ').strip().lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('What day of the week would you like to filter by? (Monday, Tuesday, etc... or "all"): ').strip().lower()

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
    try:
        df = pd.read_csv(CITY_DATA[city])
    except KeyError:
        print('You entered an invalid city name.\n\n')
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['month'] = df['Start Time'].dt.month
    df['day'] = df['Start Time'].dt.weekday
    if month != 'all':
        try:
            month = months.index(month)
            df = df[df['month'] == month +1]
            print('Filtering by month: {}'.format(months[month].title()))
        except ValueError:
            print('You entered an invalid month, continuing without filtering.')
    if day != 'all':
        try:
            day = weekdays.index(day)
            df = df[df['day'] == day +1]
            print('Filtering by weekday: {}'.format(weekdays[day].title()))
        except ValueError:
            print('You entered an invalid day of the week, continuing without filtering.')
    print('-'*40)

    read = 'yes'
    lines = 0
    while read == 'yes' and lines < len(df):
        lines += 5
        print(df[lines-5:lines])
        read = input('Would you like to see 5 more lines of data? (yes/no) ').strip().lower()

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print('The most common month is: {}'.format(months[df['month'].mode()[0]-1].title()))

    # display the most common day of week
    print('The most common day of the week is: {}'.format(weekdays[df['day'].mode()[0]-1].title()))

    # display the most common start hour
    print('The most common start hour is: {}:00hrs'.format(df['Start Time'].dt.hour.mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('The most common start station is {}.'.format(df['Start Station'].value_counts().index[0]))

    # display most commonly used end station
    print('The most common end station is {}.'.format(df['End Station'].value_counts().index[0]))

    # display most frequent combination of start station and end station trip
    #print('The most common combination of start and end stations are:  {}'.format(zip(df['Start Station'], df['End Station']).value_counts().index[0]))


    station_freq = {}
    for sstation, estation in zip(df['Start Station'], df['End Station']):
        station_freq[sstation+' // '+estation] = station_freq.get(sstation+' // '+estation,0) + 1
    most_freq = 0
    for station, freq in station_freq.items():
        if freq >= most_freq:
            most_freq = freq
    most_freq_station = []
    for station, freq in station_freq.items():
        if freq == most_freq:
            most_freq_station.append(station)
    print('The most common combination of start and end stations are:\n    {}'.format(str(most_freq_station)))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    df['trip_time'] = (df['Trip Duration']/60)
    print('The total time traveled during this period was: {}'.format(pd.Timedelta(df['trip_time'].sum(),unit='m')))
    # display mean travel time
    print('The average trip length was: {} minutes'.format(round(df['trip_time'].mean(),2)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('This is the breakdown of users and subscribers for this period: \n{}\n'.format(df['User Type'].value_counts()))

    # Display counts of gender
    try:
        print('This is the breakdown male and female riders for this period: \n{}\n'.format(df['Gender'].value_counts()))
    except KeyError:
        print('There is no gender data for this city')


    # Display earliest, most recent, and most common year of birth
    try:
        print('The earliest year of birth for riders during this period is: {}'.format(int(df['Birth Year'].min())))
        print('The latest year of birth for riders during this period is: {}'.format(int(df['Birth Year'].max())))
        print('The most common year of birth for riders during this period is: {}'.format(int(df['Birth Year'].mode())))
    except KeyError:
        print('There is no birth year data for this city')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
