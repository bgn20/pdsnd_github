import time
import pandas as pd
import numpy as np
import os


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
months = ['january', 'february', 'march', 'april', 'may', 'june']
dfColumns = ['Start Time', 'End Time', 'Trip Duration', 'Start Station', 'End Station', 'User Type', 'Gender', 'Birth Year' ]

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
    city = input("Which city do you want to search in -- chicago, New york city, washington or all?")

    # get user input for month (all, january, february, ... , june)
    month = input("Which month do you want to search for?")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("Which day do you want to search for?")

    print('-'*40)
    return city.lower(), month.lower(), day.lower()

def check_dfColumns(df):
    """checks for any missing columns and adds them into dataframe."""
    for column in dfColumns:
        if column not in df.columns:
            df[column] = np.nan
    return df

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

    if city == "all":
        """read the csv files only from current working directory for loading into dataframe."""
        path = os.getcwd()
        files = os.listdir(path)

        files_csv = [f for f in files if f[-3:] == 'csv']
        dfAll = pd.DataFrame(columns = dfColumns)
        for filename in files_csv:
            df = pd.read_csv(filename, index_col=None, header=0, encoding='utf-8-sig', engine='python', skipinitialspace=True)
            dfAll = dfAll.append(check_dfColumns(df))
        df = dfAll
    else:
       filename = CITY_DATA.get(city)
       df = pd.read_csv(filename, index_col=None, header=0, encoding='utf-8-sig', engine='python', skipinitialspace=True)
       df = check_dfColumns(df)


    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day of week'] = df['Start Time'].dt.weekday
    df['hour'] = df['Start Time'].dt.hour

    if month != 'all':
        # use the index of the months list to get the corresponding int
        inMonth = months.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['month'] == inMonth]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day of week'] == days.index(day)]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    commonMonth = df['month'].value_counts().idxmax() - 1

    print('The most common month is ',str(months[commonMonth]))

    # display the most common day of week
    commonDay = df['day of week'].value_counts().idxmax()
    print('The most common day of week is ',str(days[commonDay]))

    # display the most common start hour
    commonHour = df['hour'].value_counts().idxmax()


    if(commonHour > 12):
        commonHour -= 12
        am_or_pm = "PM"
    else:
        am_or_pm = "AM"

    print('The most common hour is {} {}'.format( commonHour, am_or_pm))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("The most commonly used start station is {}".format(df['Start Station']. value_counts(). idxmax()))

    # display most commonly used end station
    print("The most commonly used end station is {}".format(df['End Station']. value_counts(). idxmax()))

    # display most frequent combination of start station and end station trip
    print("The most commonly used combination stations are {}".format(df.groupby('Start Station')['End Station'].value_counts().idxmax()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time = df['Trip Duration'].sum()
    print('The total time travelled is {}'.format(total_time))

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('The mean time travelled is {}'.format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('\nCalculating counts of user types...\n')
    #print(df.groupby('User Type').count())
    print(df['User Type'].value_counts())

    # Display counts of gender
    print('\nCalculating counts of gender...\n')
    #print(df.groupby('Gender').count())
    print(df['Gender'].value_counts(dropna=False))

    # Display earliest, most recent, and most common year of birth
    earliest_year = df['Birth Year'].min()

    if (str(earliest_year) != "nan"):
         print("Earliest birth is in the year {}".format(str(int(df['Birth Year'].min()))))
         print("Most recent birth is in the year {}".format(str(int(df['Birth Year'].max()))))
         print("Most common year of birth is the year {}".format(str(int(df['Birth Year'].value_counts().idxmax()))))
    else:
        print("Data not available for earliest, recent and most common birth year")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def check_inputs(city, month, day):
    """Will check for whether all inputs are correct."""
    return check_input("city", city, CITY_DATA) and check_input("month", month, months) and check_input("day", day , days)


def check_input(filterName, filterValue, values):
    """Will check for each filtername and its value to ensure input is correct."""

    if (filterValue == "all"):
        return True

    inputGood = False
    for key in values:
        if key == filterValue.lower():
            return True
    return inputGood

def main():
    while True:
        city, month, day = get_filters()
        if (check_inputs(city, month, day)):
            df = load_data(city, month, day)
            i = 20
            """Will keep displaying the data until user enters no."""
            while(i < df.shape[0]):
                seeOutput = input(" Do you wish to see the data: Enter yes or no")
                if(seeOutput == "yes"):
                    print(df.head(i))
                    i += 20
                else:
                    break
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)

            restart = input('\nWould you like to restart? Enter yes or no.\n')
            if restart.lower() != 'yes':
                break
        else:
            restart = input('\nYou have entered the wrong input. Would you like to restart? Enter yes or no.\n')
            if restart.lower() != 'yes':
                break



if __name__ == "__main__":
	main()
