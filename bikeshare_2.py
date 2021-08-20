import time
import pandas as pd
import numpy as np

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
    city = ' '
    
    while city not in ['chicago','new york city','washington']:
        city = input("Which city would you like information on (chicago, new york city, washington)? ")
        city = city.lower()
        
    # TO DO: get user input for month (all, january, february, ... , june)
    month = ' '
    
    while month not in ['all','january','february','march','april','may','june']:
        month = input("Which month would you like information on (all, january, february, ... , june)? ")
        month = month.lower()

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = ' '
    
    while day not in ['all','monday','tuesday','wednesday','thursday','friday','saturday','sunday']:
        day = input("Which day of the week would you like information on (all, monday, tuesday, ... sunday)? ")
        day = day.lower()

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

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # TO DO: display the most common month
    
    df['month'] = df['Start Time'].dt.month
    month_index = df['month'].mode()[0] - 1
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    popular_month = months[month_index]
    print('Most Common Start Month: {}'.format(popular_month))
    
    # TO DO: display the most common day of week
    
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    popular_day = df['day_of_week'].mode()[0]
    print('Most Common Start Day: {}'.format(popular_day))

    # TO DO: display the most common start hour
    
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most Common Start Hour: {}'.format(popular_hour))

    print("\nThis took %s seconds." % round((time.time() - start_time),2))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    start_types = df['Start Station'].value_counts()
    start_types = start_types.nlargest(1)
    start_types = start_types.keys()[0]
    print('Most Common Start Station: {}'.format(start_types))

    # TO DO: display most commonly used end station
    end_types = df['End Station'].value_counts()
    end_types = end_types.nlargest(1)
    end_types = end_types.keys()[0]
    print('Most Common End Station: {}'.format(end_types))

    # TO DO: display most frequent combination of start station and end station trip
    station_types = 'Start Station: ' + df['Start Station'].astype(str) + ', End Station: ' + df['End Station'].astype(str)
    station_types = station_types.value_counts()
    station_types = station_types.nlargest(1)
    station_types = station_types.keys()[0]
    print('Most Frequent Combination: {}'.format(station_types))

    print("\nThis took %s seconds." % round((time.time() - start_time),2))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel = df['Trip Duration'].sum()
    print('Total Travel Time: {} seconds'.format(total_travel))

    # TO DO: display mean travel time
    mean_travel = df['Trip Duration'].mean()
    print('Mean Travel Time: {} seconds'.format(mean_travel))

    print("\nThis took %s seconds." % round((time.time() - start_time),2))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types.to_frame(), '\n')

    # TO DO: Display counts of gender
    if 'Gender' in df:
        gender_types = df['Gender'].value_counts()
        print(gender_types.to_frame(), '\n')
    else:
        print('Gender stats cannot be calculated because Gender does not appear in the dataframe\n')

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        earliest_birth = df['Birth Year'].sort_values()
        earliest_birth_key = earliest_birth.keys()[0]
        earliest_birth = earliest_birth[earliest_birth_key]
        print('Earliest Year of Birth: ', earliest_birth.astype(int))

        recent_birth = df['Birth Year'].sort_values(ascending=False)
        recent_birth_key = recent_birth.keys()[0]
        recent_birth = recent_birth[recent_birth_key]
        print('Most Recent Year of Birth: ', recent_birth.astype(int))

        common_birth = df['Birth Year'].value_counts()
        common_birth = common_birth.nlargest(1)
        common_birth = common_birth.keys()[0]
        print('Most Common Year of Birth: ', common_birth.astype(int))
    else:
        print('Birth Year stats cannot be calculated because Birth Year does not appear in the dataframe')

    print("\nThis took %s seconds." % round((time.time() - start_time),2))
    print('-'*40)
    

def display_data(df):
    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no. \n')
    view_data = view_data.lower()
    start_loc = 0
    while (view_data != 'no'):
        print(df.iloc[start_loc:(start_loc + 5)])
        start_loc += 5
        view_display = input('Do you wish to continue?: ').lower()
        view_data = view_display
    
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
