import requests
import json
from urllib.parse import urlparse, parse_qs
from config import stable_base_url, API_KEY, API_PASSWORD

def get_order_data(start_date, end_date,test):
    """
    Retrieve order data from the Shopify API for a given date range

    Args:
        start_date (str): Start date in the format "YYYY-MM-DDTHH:MM:SS+HH:MM"
        end_date (str): End date in the format "YYYY-MM-DDTHH:MM:SS+HH:MM"
        test (bool): Specifies whether it's a test run without saving the Excel file


    Returns:
        dict: Dictionary containing the retrieved order data
    """

    if test:
        limit = 250
        financial_status = "paid"
        fulfillment_status = "any"


        first_params = {

            "status": fulfillment_status,
            "financial_status": financial_status,
            "limit": limit,
            "created_at_min": start_date,
            "created_at_max": end_date
        }
        first_response = requests.get(stable_base_url + "/orders.json" , auth=(API_KEY, API_PASSWORD), params=first_params)

         # Get the data from the response
        response = first_response


        if response.status_code == 200:
            # Process the returned data as needed
            return(f"API GET request for order data json data is successful with status code: {response.status_code}")

        else:
            # API call encountered an error
            return(f"API call failed with status code: {response.status_code}")


    else:
        # Set the page to 1 and the limit to 250
        limit = 250
        financial_status = "paid"
        fulfillment_status = "any"


        first_params = {

            "status": fulfillment_status,
            "financial_status": financial_status,
            "limit": limit,
            "created_at_min": start_date,
            "created_at_max": end_date
        }
        first_response = requests.get(stable_base_url + "/orders.json" , auth=(API_KEY, API_PASSWORD), params=first_params)

        data = first_response.json()

        try:
            link = first_response.headers['Link']
        except:
            return data
        count = 0
        while link:
            parse_result = urlparse(link)

            dict_result = parse_qs(parse_result.query)
            try:
                page_info = dict_result['page_info'][count]
            except:
                break


            page_info = page_info.split('>')[0]

            params = {
                "page_info": page_info,
                "limit": limit
            }

            response = requests.get(stable_base_url + "/orders.json", auth=(
                API_KEY, API_PASSWORD), params=params)
            temp_data = response.json()
            data["orders"] += temp_data["orders"]


            link = response.headers['Link']
            if count == 0:
                count += 1


        return data
