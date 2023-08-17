import time
import pandas as pd

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
    
    cities = ['chicago', 'new york city', 'washington']
    # get user input for city (chicago, new york city, washington)
    global city
    city = str(input('Would you like to see data for Chicago, New York city, or Washington? ')).lower()
    # Use a while loop to handle invalid inputs
    while city not in cities:
       city = str(input('Attention! Your input must be one of the three cities: Chicago, New York city, or Washington. ')).lower()
    
    months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    # get user input for month (all, january, february, 'march', 'april', 'may', june)
    month = str(input('If you want to filter the data by month, please input one of the first 6 months in letters. If not, please input "all" ')).lower()
    while month not in months:
        month = str(input('Attention! Your input must be one of the first 6 months in letters or "all" ')).lower()
    
    days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    # get user input for day of week (all, monday, tuesday, 'wednesday', 'thursday', 'friday', 'saturday', sunday)
    day = str(input('If you want to filter the data by day of week, please input the day. If not, please input "all" ')).lower()
    while day not in days:
        day = str(input('Attention! Your input must be one of the week days or "all" ')).lower()
    
    print('Hello! Let\'s explore some US bikeshare data!')
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
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    #create the start hour column
    df['start hour'] = df['Start Time'].dt.hour

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

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

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    months = ['0', 'january', 'february', 'march', 'april', 'may', 'june']
    print('The most common month is {}'.format(months[df['month'].mode()[0]]))

    # display the most common day of week
    print('The most common day of week is {}'.format(df['day_of_week'].mode()[0]))

    # display the most common start hour
    print('The most common start hour is {}'.format(df['start hour'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('The most common start station is {}'.format(df['Start Station'].mode()[0]))

    # display most commonly used end station
    print('The most common end station is {}'.format(df['End Station'].mode()[0]))

    # display most frequent combination of start station and end station trip
    df['Trip'] = df['Start Station'] + ' to ' + df['End Station']
    print('The most frequent trip is from {}'.format(df['Trip'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('Total travel time is {} seconds'.format(df['Trip Duration'].sum()))

    # display mean travel time
    print('Mean travel time is {} seconds'.format(int(df['Trip Duration'].mean())))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types and counts of gender
    print('Counts of user types:\n', df['User Type'].value_counts())

    # Display counts of gender, earliest, most recent, and most common year of birth
    if city != 'washington':
        print('Counts of gender:\n', df['Gender'].value_counts())
        print('Earliest year of birth: {}'.format(int(df['Birth Year'].min())))
        print('Most recent year of birth: {}'.format(int(df['Birth Year'].max())))      
        print('Most common year of birth: {}'.format(int(df['Birth Year'].mode())))

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

        # Display 5 lines of raw data upon request by the user
        row_data = input('\nWould you like to see 5 lines of row data? Please enter yes or no.\n').lower()
        while row_data not in ['yes', 'no']:
            row_data = input('Attention! The answer should be yes or no.\n').lower()
        index = 0
        while row_data == 'yes' and index+5 <= df.shape[0]:
            print(df.iloc[index:index+5])
            row_data = input('\nWould you like to see more 5 lines of row data? Please enter yes or no.\n').lower()
            while row_data not in ['yes', 'no']:
                row_data = input('Attention! The answer should be yes or no.\n').lower()
            index += 5
        if index+5 > df.shape[0]:
            print(df.iloc[index:df.shape[0]])
            print('End of data')
            
        # Ask the user if they like to restart
        restart = input('\nWould you like to restart? Enter yes or no.\n').lower()
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
