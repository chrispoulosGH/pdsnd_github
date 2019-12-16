import time
import pandas as pd
import numpy as np
import statistics as st

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv',
              'test': 'test.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    try:
        # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
       while True:
          city = input('Enter a valid city (chicago, new york city or washington).\n')
          if city.lower() in ['all','chicago','new york city','washington']:
             break

   # get user input for month (all, january, february, ... , june)

       while True:
          month = input('Enter a valid month (all, january, february, ... , june).\n')
          if month.lower() in ['all','january','february','march','april','may','june']:
             break

    # get user input for day of week (all, monday, tuesday, ... sunday)
       while True:
          day = input('Enter a valid day of week (all, monday, tuesday, ... sunday).\n')
          if day.lower() in ['all','monday','tuesday','wednesday','thursday','friday','saturday','sunday']:
             break

    except Exception as e:
        print('\nError encountered processing user input: {}.'.format(e))
        raise

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

    # load data file into a dataframe
    try:
        df = pd.read_csv(CITY_DATA[city])

        # convert the Start Time column to datetime
        df['Start Time'] = pd.to_datetime(df['Start Time'])

        # extract month and day of week from Start Time to create new columns
        df['month'] = df['Start Time'].dt.month
        df['day_of_week'] = df['Start Time'].dt.weekday_name

        # filter by month if applicable
        if month != 'all':
            # use the index of the months list to get the corresponding int
            months = ['january', 'february', 'march', 'april', 'may', 'june']
            month = months.index(month) + 1

            # filter by month to create the new dataframe
            df = df[df['month'] == month]

        # filter by day of week if applicable
        if day != 'all':
            # filter by day of week to create the new dataframe
            df = df[df['day_of_week'] == day.title()]

    except Exception as e:
        print('\nError encountered processing loading data files: {}.'.format(e))
        raise

    return df

def convert_time(time):
    """convert 24 hour to standard time."""
    try:
        if time==24:
            return "{}{}".format(time-12," Midnight")
        if time > 12:
            return "{}{}".format(time-12,' PM')
        if time < 12:
            return "{}{}".format(time,' AM')
        if time == 12:
            return "{}{}".format(time," Noon")

    except Exception as e:
        print('\nError encountered in time conversion: {}.'.format(e))
        raise





def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    try:
        print('\nCalculating The Most Frequent Times of Travel...\n')
        start_time = time.time()
        months = ['January', 'February', 'March', 'April', 'May', 'June']

        # display the most common month
        print("The most common month is {}.".format(months[df['month'].mode()[0]-1]))

        # display the most common day of week
        print("The most common day of week is {}.".format(df['day_of_week'].mode()[0]))

        # display the most common start hour
        df['start_hour'] = df['Start Time'].dt.hour
        print("The most common start hour is {}.".format(convert_time(df['start_hour'].mode()[0])))

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)

    except Exception as e:
        print('\nError encountered processing time stats: {}.'.format(e))
        raise

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    try:
        print('\nCalculating The Most Popular Stations and Trip...\n')
        start_time = time.time()

        # display most commonly used start station
        print("Most commonly used Start Station is {}.".format(df['Start Station'].mode()[0]))

        # display most commonly used end station
        print("Most commonly used End Station is {}.".format(df['End Station'].mode()[0]))

        # display most frequent combination of start station and end station trip
        df['start_end_station'] = df['Start Station'] + ' to ' + df['End Station']
        print("Most frequent combination of start station and end station trips is {}.".format(df.start_end_station.mode().iloc[0]))

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)

    except Exception as e:
        print('\nError encountered processing station stats: {}.'.format(e))
        raise


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['Duration']=df['End Time']-df['Start Time']

    duration_sum=df['Duration'].sum()
    print("Total Travel Time {} days, {} hours and {} minutes.".format(duration_sum.components.days,duration_sum.components.hours,duration_sum.components.minutes))

    duration_mean=df['Duration'].mean()
    print("Mean Travel Time {} days, {} hours and {} minutes.".format(duration_mean.components.days,duration_mean.components.hours,duration_mean.components.minutes))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    try:
       df['User_Type']=df['User Type']
       for i, r in df['User_Type'].value_counts().iteritems():
         print("There are {} {} users.".format(r,i))
    except Exception as e:
        print('\nError Encountered processing User Type stats: {}'.format(e))

    # Display counts of gender
    try:
       print('\n')
       for i, r in df['Gender'].value_counts().iteritems():
         print("There are {} {} users.".format(r,i))
    except Exception as e:
        print('\nError Encountered processing Gender stats: {}.'.format(e))

    # Display earliest, most recent, and most common year of birth
    try:
       print("\nThe earliest user year of birth is {}.".format(str(df['Birth Year'].min()).split('.')[0]))
       print("The most recent user year of birth is {}.\n".format(str(df['Birth Year'].max()).split('.')[0]))

       for i, r in (df['Birth Year'].mode().value_counts().iteritems()):
         print("The most common occurence/s of year of birth is {}.".format(str(i).split('.')[0]))

    except Exception as e:
       print('\nError Encountered processing Birth Year stats: {}.'.format(e))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    """diplay 5 records at a time moving or forward back dependent on user input."""
    try:
        begin=0

        prev_direction='f'
        print('Raw Data Display')
        pageSize=int(input('Enter in a numeric for page size. '))
        end=pageSize-1
        while True:
            ans=input('Enter F to page {} records forward, B to page {} records back, N to stop.'.format(pageSize,pageSize))
            if ans.lower()=='n':
                break;
            if ans.lower()=='f':
                if prev_direction=='b':
                   begin+=pageSize               #move fwd 5 from prev direction adjustment
                   end+=pageSize
                prev_direction='f'
                print(df.loc[begin:end])
                begin+=pageSize
                end+=pageSize
            if ans.lower()=='b':
                if prev_direction=='f':   #move back 5 from prev direction adjustment
                    begin-=pageSize
                    end-=pageSize
                    prev_direction='b'
                if end<=pageSize-1:                #adjust if pointer is at read size or less
                    begin=0
                    end=pageSize-1
                else:
                    begin-=pageSize
                    end-=pageSize
                    print(df.loc[begin:end])

    except Exception as e:
       print('\nError encountered displaying raw data: {}.'.format(e))
       raise

def main():
    restart='x'
    while True:
        try:
            city, month, day = get_filters()
            df = load_data(city, month, day)
            #city='test'
            print("Processing data for the city of {}.\n".format(city.title()))
            #df = load_data('test', 'all', 'all')
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)
            display_data(df)

            while True:
              restart = input('\nWould you like to restart? Enter y or n.\n')
              if restart.lower() in ['n','y']:
                break

            if restart.lower() == 'n':
                break


        except Exception as e:
            print('\nError Encountered : {}\n'.format(e))


if __name__ == "__main__":
	main()
