import requests
import pandas as pd

from urllib.parse import urlparse, parse_qs
from pathlib import Path
from config import stable_base_url, API_KEY, API_PASSWORD




def get_all_products_details(folder, test):
    """
    Retrieves details of all products from the Shopify API and saves them to an Excel file.

    Parameters:
    - folder (str): The folder path where the Excel file will be saved.
    - test (bool): Specifies whether it's a test run without saving the Excel file.

    Returns:
    - str: A success or error message indicating the result of the API call.
    """

    if test and folder == None:
        headers = {
            "Content-Type": "application/json",
        }

        # Send the API request
        first_response = requests.get(stable_base_url + "/products.json", auth=(API_KEY, API_PASSWORD), headers=headers)

        # Get the data from the response
        response = first_response


        if response.status_code == 200:
            # Process the returned data as needed
            return(f"API GET request for all product json data is successful with status code: {response.status_code}")

        else:
            # API call encountered an error
            return(f"API call failed with status code: {response.status_code}")



    else:
        headers = {
            "Content-Type": "application/json",
        }

        # Send the API request
        first_response = requests.get(stable_base_url + "/products.json", auth=(API_KEY, API_PASSWORD), headers=headers)

        # Get the data from the response
        data = first_response.json()
        link = first_response.headers['Link']

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
            }

            response = requests.get(stable_base_url + "/products.json", auth=(
                API_KEY, API_PASSWORD), params=params)
            temp_data = response.json()
            data["products"] += temp_data["products"]


            link = response.headers['Link']
            if count == 0:
                count += 1



        # Create an empty list to store the product data
        product_data = []

        # Iterate through the products and store the name and id in the list
        for product in data["products"]:
            product_data.append({
            "name": product["title"],
            "id": product["id"]
            })

        # Create a dataframe from the product data
        df = pd.DataFrame(product_data)

        df = df.sort_values("id")

        path = Path(folder + '/AllProductDetails.xlsx')
        df.to_excel(path)
