import time
import pandas as pd

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
Months = ['january', 'february', 'march', 'april', 'may', 'june']
Weekend_days = ['monday', 'tuesday', 'wednesday', 'thuresday', 'friday', 'saturday', 'sunday']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    while True :
        print('Hello! Let\'s explore some US bikeshare data!')
        # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
        city = input('Enter the city you interseted in (chicago, new york city, washington)\n').lower()
        while CITY_DATA.get(city,0) == 0 :
            print('You Entered invalid city name ,you should enter a valid city name from (chicago, new york city, washington) \n').lower()

        # get user input for month (all, january, february, ... , june)

        month = input('Enter the month you interseted in (january, february, march, april, may, june) or all \n').lower()
        while(month not in Months) and month != 'all' :
            month = input('You entered an invalid Month name , you should enter a valid month name or \n').lower()

        # get user input for day of week (all, monday, tuesday, ... sunday)
        day = input('Enter the day of week you interseted in (monday, tuesday, wednesday, thuresday, friday, saturday, sunday) or all\n').lower()
        while(day not in Weekend_days) and day != 'all':
            day = input('You entered an invalid Day name, you should enter a valid day name or all\n').lower()
            continue
        break
    print('-'*140)
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
    file_data = pd.read_csv(CITY_DATA[city])
    df = pd.DataFrame(data=file_data)

    # weekday and month columns
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month

    df['weekend_day'] = df['Start Time'].dt.day_name()

    if month != 'all':
        df = df[df['month']==Months.index(month) + 1]


    if day != 'all':
        df = df[df['weekend_day'] == day.title()]


    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_months = df['month'].value_counts()
    print("Most Popular Month : {} , Count: {}".format(Months[most_common_months.index[0] - 1],most_common_months.iloc[0]))

    # display the most common day of week
    most_common_days = df['weekend_day'].value_counts()
    print("Most Popular Day : {} , Count: {}".format(most_common_days.index[0], most_common_days.iloc[0]))


    # display the most common start hour
    most_common_hours = df['Start Time'].dt.hour.value_counts()
    print("Most Popular Hour : {} , Count: {}".format(most_common_hours.index[0], most_common_hours.iloc[0]))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*140)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_sstations = df['Start Station'].value_counts()
    print("Most commonly used start station : {} , Count: {}".format(most_common_sstations.index[0], most_common_sstations.iloc[0]))

    # display most commonly used end station
    most_common_estations = df['End Station'].value_counts()
    print("Most commonly used end station : {} , Count: {}".format(most_common_estations.index[0], most_common_estations.iloc[0]))


    # display most frequent combination of start station and end station trip
    secomp = df.groupby(['Start Station','End Station']).size().reset_index(name="counts")
    max_row_id = secomp['counts'].idxmax()
    print('most frequent combination of start station and end station trip is : {} and {} , Counts : {}'.format(secomp['Start Station'].iloc[max_row_id], secomp['End Station'].iloc[max_row_id],secomp['counts'].iloc[max_row_id]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*140)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    df['travel_time'] = (pd.to_datetime(df['End Time']) - df['Start Time']).dt.total_seconds()
    print('total travel time is : {} seconds'.format(df['travel_time'].sum()))


    # display mean travel time
    print('mean travel time is : {} seconds'.format(df['travel_time'].mean()))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*140)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('Counts of Subscriber : {} , Customer : {} , Dependent : {}'.format(user_types['Subscriber'], user_types['Customer'], user_types['Dependent']))


    # Display counts of gender
    if city != 'washington' :
        gender_counts = df['Gender'].value_counts()
        print('Counts of Males : {} , Females : {} '.format(gender_counts['Male'],gender_counts['Female']))


    # Display earliest, most recent, and most common year of birth
    if city != 'washington' :
        print('earliest year of birth : {} , most recent year of birth : {} , most common year of birth : {} '.format(df['Birth Year'].min(), df['Birth Year'].max(), df['Birth Year'].value_counts().index[0]))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*140)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        display_data(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

def display_data(df):
    """[display_data]: ask user for display  5 rows in dataframe

    Args:
        df ([DataFrame]): dataframe data to be displayed
    """
    index=0
    user_input=input('would you like to display 5 rows of raw data?\n').lower()
    while user_input in ['yes','y','yep','yea'] and index+5 < df.shape[0]:
        print(df.iloc[index:index+5])
        index += 5
        user_input = input('would you like to display more 5 rows of raw data?\n').lower()

if __name__ == "__main__":
	main()
