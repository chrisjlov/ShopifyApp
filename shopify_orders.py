## ---------------------------
##
## Script name: shopify_orders.py
##
## Purpose of script: Sets Shopify Order JSON data into dataframe
##
## Author: Chris Lovett
##
## Date Created: 2022-10-30
##
## Copyright (c) Chris Lovett, 2022
##
## ---------------------------
import requests
import pandas as pd


from datetime import date
from convert_time import *
from get_order_data import *
from config import stable_base_url,API_KEY, API_PASSWORD



def get_order_count(date_min, date_max):
    """
    Makes a request to the Shopify API to retrieve the number of orders with a "paid" financial status
    that were created between the specified date_min and date_max timestamps.

    Parameters:
        date_min (str): The start timestamp for the time period to retrieve orders from, in ISO-8601 format.
        date_max (str): The end timestamp for the time period to retrieve orders from, in ISO-8601 format.

    Returns:
        int: The count of orders.
    """

    #Shopify API request parameters
    params = {
        "status": "unfulfilled",
        "financial_status": "paid",
        "created_at_min": date_min,
        "created_at_max": date_max
    }

    r = requests.get(stable_base_url + "/orders/count.json", auth=(API_KEY, API_PASSWORD), params=params)

    return r.json()['count']

def get_orders_today():
    """
    Retrieves the orders that were created today.

    Returns:
        tuple: A tuple containing the following elements:
            - data (dict): The data for the orders created today.
            - count_orders (int): The count of orders created today.
    """

    todayMin, todayMax = convert_to_UTC(date.today(),date.today())
    print("Fetching orders from ", todayMin, " to ", todayMax)

    count_orders = get_order_count(todayMin, todayMax)
    data = get_order_data(todayMin, todayMax, False)

    return  data, count_orders


def get_orders_two_dates(date_first, date_second):
    """
    Retrieves the orders created between the specified dates.

    Parameters:
        date_first (datetime.date): The start date for the time period to retrieve orders from.
        date_second (datetime.date): The end date for the time period to retrieve orders from.

    Returns:
        tuple: A tuple containing the following elements:
            - data (dict): The data for the orders created between the specified dates.
            - count_orders (int): The count of orders created between the specified dates.
    """

    date_min, date_max = convert_to_UTC(date_first, date_second)
    print("Fetching orders from ", date_min, " to ", date_max)

    count_orders=get_order_count(date_min,date_max)
    data = get_order_data(date_min,date_max, False)

    return data,  count_orders

global list_product_ids
def sort_orders(orders_JSON_data):
    """
    Sorts the orders in a JSON object by product ID and creates a Pandas dataframe containing information about
    the products in each order. It also creates a list of unique product IDs.

    Parameters:
        orders_JSON_data (dict): A JSON object containing order data.

    Returns:
        tuple: A tuple containing the following elements:
            - order_DF (pandas.DataFrame): A dataframe containing information about the products in each order.
            - list_product_ids (list): A list of unique product IDs.
    """

    global  order_DF, list_product_ids, list_product_names
    list_product_ids = []
    list_product_names = []
    order_DF = pd.DataFrame(columns=('productID','productName','order_ID','orderNumber','quantity', 'variantID','size','id'))

    count = 0
    for order in orders_JSON_data['orders']:
        order_ID = order['id']
        order_Number = order['order_number']


        for product in order['line_items']:
            list_product_ids.append(str(product['product_id']))
            order_DF.loc[count]= (product['product_id'], product['name'], order_ID, order_Number,  product['quantity'], product['variant_id'], product['variant_title'], product['id'])
            count+=1



    list_product_ids.sort()
    order_DF = order_DF.sort_values(by = 'productID')
    order_DF = order_DF.reset_index(drop=True)


    print(order_DF)
    return order_DF, list_product_ids


def get_product_ID_DataFrame():
    """
    Creates a Pandas dataframe containing the unique product IDs and the number of times each product appears
    in the list of product IDs.

    Returns:
        pandas.DataFrame: A dataframe containing the unique product IDs and the number of times each product appears
            in the list of product IDs.
    """

    product_quantities_DF = pd.DataFrame(columns=('productID', 'productName' ,'Quantity'))
    product_ids_filter = []
    for id in list_product_ids:
        temp_order_df = order_DF
        temp_order_df = temp_order_df.drop_duplicates(subset='productID')

        temp_product_name = temp_order_df.loc[temp_order_df['productID']==int(id)]
        temp_product_name = temp_product_name['productName']
        temp_product_name = str(temp_product_name.iloc[0])
        temp_product_name = temp_product_name.strip()

        if "- S" in temp_product_name:
            product_name = temp_product_name.replace("- S", "")
        elif "- M" in temp_product_name:
            product_name = temp_product_name.replace("- M", "")
        elif "- L" in temp_product_name:
            product_name = temp_product_name.replace("- L", "")
        elif "- XL" in temp_product_name:
            product_name = temp_product_name.replace("- XL", "")
        elif "- XXL" in temp_product_name:
            product_name = temp_product_name.replace("- XXL", "")
        elif "- XXXL" in temp_product_name:
            product_name = temp_product_name.replace("- XXXL", "")
        else:

            product_name = temp_product_name

        if id in product_quantities_DF['productID'].values and product_name in product_quantities_DF['productName'].values:

            product_quantities_DF.loc[product_quantities_DF['productID'] == id, 'Quantity'] += 1
        elif id not in product_quantities_DF['productID'].values and product_name not in product_quantities_DF['productName'].values:

            new_row = pd.DataFrame({'productID': [id], 'productName': product_name, 'Quantity': [1]})

            product_quantities_DF = pd.concat([product_quantities_DF, new_row], ignore_index=True)
            product_ids_filter.append(id)

    # product_dict = dict(zip(product_ids_filter, ))
    product_quantities_DF = product_quantities_DF.reset_index(drop=True)
    print(product_quantities_DF)
    return product_quantities_DF

def get_order_DF():
    """
    Returns the dataframe containing information about the products in each order.

    Returns:
        pandas.DataFrame: A dataframe containing information about the products in each order.
    """

    return order_DF


def sort_product_ids(list_productIDs, doubles):
    """
    Sort a list of product IDs and return a list with or without duplicates.

    This function takes a list of product IDs and returns a new list with or without
    duplicates, depending on the value of the `doubles` parameter. If `doubles` is
    `True`, the function returns a list without duplicates and a list of the indexes
    of the duplicates in the original list. If `doubles` is `False`, the function
    returns a list without duplicates.

    Args:
        list_productIDs (list): The list of product IDs.
        doubles (bool): A flag indicating whether to include duplicates or not.

    Returns:
        tuple: A tuple containing a list without duplicates and a list of the indexes
            of the duplicates in the original list, if `doubles` is `True`. If
            `doubles` is `False`, a list without duplicates is returned.
    """

    if doubles:
        # Create an empty list to store the indexes of the duplicates
        list_duplicate_indexes = []

        # Create a set to keep track of the items that have been seen
        seen = set()

        # Iterate over the list
        for i, item in enumerate(list_productIDs):
            # If the item has not been seen before
            if item not in seen:
                # Add it to the set of seen items
                seen.add(item)
            # If the item has been seen before
            else:
                # Add its index to the list of duplicate indexes
                list_duplicate_indexes.append(i)

        # Create a new list without the duplicates
        list_noDuplicates = []
        for i, item in enumerate(list_productIDs):
            if i not in list_duplicate_indexes:
                list_noDuplicates.append(item)

        return list_noDuplicates, list_duplicate_indexes

    else:
        return list(set(list_productIDs))

