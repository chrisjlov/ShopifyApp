import datetime
import pytz
import requests
from requests.exceptions import RequestException

def get_latest_api_version(base_url, API_KEY, API_PASSWORD):
    """
    Retrieves the latest API version of Shopify from the specified base URL.

    Parameters:
    - base_url (str): The base URL for the Shopify API.
    - API_KEY (str): The API key for authentication.
    - API_PASSWORD (str): The API password for authentication.

    Returns:
    - str or None: The URL for the latest API version if the API call is successful, otherwise None.
    """


    current_date = datetime.datetime.now(pytz.utc)
    current_year = current_date.year
    current_month = current_date.month
    current_day = current_date.day
    current_hour = current_date.hour

    if current_month in [1, 2, 3]:
        latest_version_month = 1
    elif current_month in [4, 5, 6]:
        latest_version_month = 4
    elif current_month in [7, 8, 9]:
        latest_version_month = 7
    else:
        latest_version_month = 10

    if current_month == latest_version_month and current_day == 1 and current_hour >= 17:
        latest_version_month += 3
        if latest_version_month > 12:
            latest_version_month = 1
            current_year += 1

    # Format the version as YYYY-MM
    latest_version = f"{current_year}-{str(latest_version_month).zfill(2)}"


    # Get the latest stable version
    latest_version = str(latest_version)

    # Set the base URL for the Shopify API
    url = base_url + latest_version

    # Make the API call and check for success
    response = requests.get(url, auth=(
            API_KEY, API_PASSWORD))

    if response.status_code == 200:
        # API call was successful
        data = response
        # Process the returned data as needed
        print(f"Latest API version of Shopify Successful with status code: {response.status_code}")
        return url

    else:
        # API call encountered an error
        print(f"API call failed with status code: {response.status_code}")
        return None


