import requests
import pandas as pd
import datetime
import time
from sqlalchemy import create_engine
from credentials import RAPIDAPIKEY, DB_CONNECTION_STRING


def get_market_data(symbol):
    """
    Fetch market data for a given stock symbol using the RealStonks API.

    Args:
        symbol (str): Stock symbol to fetch data for.

    Returns:
        dict or None: Market data for the specified symbol in JSON format,
                      or None if an error occurred during the API request.
    """
    # Construct the URL for the RealStonks API using the provided symbol
    url = f'https://realstonks.p.rapidapi.com/{symbol}'
    
    # Headers required for the RapidAPI request
    headers = {
      "X-RapidAPI-Key": RAPIDAPIKEY,  # Replace with your RapidAPI key
      "X-RapidAPI-Host": "realstonks.p.rapidapi.com"
    }

    # Send a GET request to the RealStonks API
    response = requests.get(url, headers=headers)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response into a dictionary and return it
        data = response.json()
        return data
    else:
        # Return None if an error occurred during the API request
        return None


def fetch_stock_data(symbols):
    """
    Fetches stock market data for a list of symbols and returns it as a DataFrame.

    Parameters:
        symbols (list): A list of stock symbols for which data is to be fetched.

    Returns:
        pandas.DataFrame: A DataFrame containing the fetched stock market data.

    Notes:
        This function assumes the existence of a 'get_market_data' function that
        retrieves data for a single symbol. It also adds a 'symbol' column to
        the DataFrame to indicate which symbol the data belongs to, and a 'date'
        column with the current timestamp.

    Example:
        data = fetch_stock_data(['TSLA', 'AAPL', 'MSFT'])
    """
    df = pd.DataFrame()

    for symbol in symbols:
        # Fetch data for the current symbol using the 'get_market_data' function
        data = get_market_data(symbol)

        if data:
            # Create a temporary DataFrame for the fetched data
            temp_df = pd.DataFrame(data, index=[0])

            # Add 'symbol' and 'date' columns to the temporary DataFrame
            temp_df['symbol'] = symbol
            temp_df['date'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # Concatenate the temporary DataFrame with the main DataFrame
            df = pd.concat([df, temp_df], ignore_index=True)

            # Pause for half a second between requests to the API
            time.sleep(0.5)

    return df


def upload_data(df, database, tablename):
    """
    Uploads a pandas DataFrame to a specified database table using SQLAlchemy.

    Args:
        df (pandas.DataFrame): The DataFrame to be uploaded.
        database (str): The name of the target database.
        tablename (str): The name of the target table in the database.

    Returns:
        None

    This function performs the following steps:
    1. Creates a SQLAlchemy database connection engine using the provided 'database' parameter.
    2. Uploads the contents of the DataFrame 'df' to the specified database table named 'tablename'.
       - If the table exists, it appends the data to it.
       - If the table does not exist, a new table with the given name is created.
    3. Retrieves the current date and time as a formatted string.
    4. Prints a success message with the timestamp and the database and table names to indicate
       that the data upload was successful.

    In case of an exception during database operations, an error message is printed.

    Example:
    >>> upload_data(my_dataframe, "my_database", "my_table")
    Data successfully uploaded to the my_database database and my_table table at: 2023-10-20 14:30:00
    """
    try:
        # Create a SQLAlchemy database connection engine
        engine = create_engine(f"{DB_CONNECTION_STRING}{database}")

        # Upload the DataFrame to the specified database table
        df.to_sql(tablename, con=engine, if_exists='append', index=False)

        # Get the current date and time
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:M:%S')

        # Print a success message with the timestamp and table name
        print(f'Data successfully uploaded to the {database} database and {tablename} table at : {now}')
    except Exception as e:
        print(f'Error: {str(e)}')


if __name__ == "__main__":

# set up infinite loop running every 60 seconds

    symbols = ['TSLA', 'MSFT', 'SPOT', 'UBER', 'AAPL']
    database = 'financialdata'
    tablename = 'financial_data'

    try:
        while True:
            upload_data(fetch_stock_data(symbols), database, tablename)
            time.sleep(60)
    except KeyboardInterrupt:
        print("Loop interrupted by KeyboardInterrupt. Exiting.")
        