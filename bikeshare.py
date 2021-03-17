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

    print('Hello! I am Macarena Viza! Let\'s explore some US bikeshare data! \n')
    #get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = ''
    
    while city not in CITY_DATA.keys():
        print('#################\n#### C I T Y ####\n#################')
        print('Which city do you want analyze?')
        city = input('Chicago, New York city or Washington \n').lower()
        if city not in CITY_DATA.keys():
            print("You have to choose a city from the options, please check your input.\n")

    #get user input for month (all, january, february, ... , june)
    month_options = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    month = ''
    while month not in month_options:
        print('###################\n#### M O N T H ####\n###################')
        print('Which month do you want analyze?')
        print('-You can choose from between January to June')
        print('-If you want view all months, write "all"')
        month = input().lower()
        if month not in month_options:
            print("You have to choose a month from the posible options, please check your input.\n")
    

    #get user input for day of week (all, monday, tuesday, ... sunday)
    day_options = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday',
            'Sunday', 'all']
    day = ''
    while day not in day_options:
        print('###############\n#### D A Y ####\n###############')
        print('Which day do you want analyze?')
        print('-You can choose a day in the week')
        print('-If you want view all days, write "all"')
        day = input().lower()
        if day not in day_options:
            print("You have to choose a day from the posible options, please check your input.\n")

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
    print('Great! go for that data!')
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month_name()
    df['day_of_week'] = df['Start Time'].dt.day_name()
    if month != 'all':
        df = df[df['month'] == month.title()]

    if day != 'all':
        df = df[df['day_of_week'] == day.title()]
        
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    #display the most common month
    popular_month = df['month'].mode()[0]
    print(f"Most Popular Month:  {popular_month}")

    #display the most common day of week
    popular_day_of_week = df['day_of_week'].mode()[0]
    print(f"Most Popular day of week:  {popular_day_of_week}")

    #display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_start_hour = df['hour'].mode()[0]
    print(f"Most Popular start hour:  {popular_start_hour}")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    #display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print(f"Most Popular start station: {popular_start_station}")

    #display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print(f"Most Popular end station: {popular_end_station}")

    #display most frequent combination of start station and end station trip
    df['Combination'] = df['Start Station'] + ' to ' + df['End Station']
    popular_combination = df['Combination'].mode()[0]
    print(f"Most Popular combination: {popular_combination}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    #display total travel time
    total_travel_time = df['Trip Duration'].sum()
    hour, minutes, seconds = convert_seconds(total_travel_time)
    print("Total travel time: %d:%02d:%02d" % (hour, minutes, seconds) )

    #display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    hour, minutes, seconds = convert_seconds(mean_travel_time)
    print("Mean travel time: %d:%02d:%02d" % (hour, minutes, seconds) )

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def convert_seconds(seconds):
    """Convert seconds to hours, minute and seconds."""
    seconds = seconds % (24 * 3600) 
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return hour, minutes, seconds

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    #Display counts of user types
    total_by_user_type = df['User Type'].value_counts()
    print(f"Counts of user types:\n{total_by_user_type}\n")

    #Display counts of gender
    try:
        total_by_gender = df['Gender'].value_counts()
        print(f"Counts of user types:\n{total_by_gender}\n")
    except:
        print("This city doesn't record data by gender") 

    #Display earliest, most recent, and most common year of birth
    try:
        earliest_birth_year = int(df['Birth Year'].min())
        recent_birth_year = int(df['Birth Year'].max())
        popular_birth_year = int(df['Birth Year'].mode())
        print(f"The earliest year of birth: {earliest_birth_year}")
        print(f"The most recent year of birth: {recent_birth_year}")
        print(f"The most common year of birth: {popular_birth_year}")
    except:
        print("This city doesn't record year of birth")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def display_data(df):
    '''Display 5 lines of raw data'''
    lines = 0
    response = ''
    response_options = ['yes', 'no']
    while response not in response_options:
        response = input('\ndo you want to see raw data? (yes/no)\n').lower()
        if response == 'yes':
            print(df.head(5))
        elif response not in response_options:
            print("you have to write yes or no, please check your response\n")

    while response == 'yes':
        response = input('do you want to see more 5 lines of raw data? (yes/no)\n').lower()
        lines += 5
        if response == 'yes':
            print(df[lines:lines+5])
        elif response == 'no':
            break
        elif response not in response_options:
            print("you have to write yes or no, please check your response\n")
            response = 'yes' #to return to: do you wat to see more 5 lines of raw data? 
            
    print('-'*40)

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
