## ---------------------------
##
## Script name: save_images.py
##
## Purpose of script: Saves order images and makes spreadsheet of all orders
##
## Author: Chris Lovett
##
## Date Created: 2022-10-30
##
## Copyright (c) Chris Lovett, 2022
##
## ---------------------------


from pathlib import Path

from show_orders import *
from convert_time import *
from shopify_orders import *
from order_data import *
import os
import shutil

def save_to_folder(date_1, date_2, folder, sorted_list_product_ids):
    """
    Save a list of product images, along with some data, to a specified folder.

    Args:
        date_1 (str): the start date of the orders
        date_2 (str): the end date of the orders
        folder (str): the path of the folder where the images and data should be saved
        sorted_list_product_ids (list): a list of product IDs to be saved

    Returns:
        None
    """

    print("Saving images to directory along with datasheets")

    start_date, end_date = convert_to_format(date_1, date_2)

    # Creates directory if not already created
    directory = 'Orders From ' + start_date+ ' To ' + end_date
    parent_directory = str(folder+'/')
    path = os.path.join(parent_directory, directory)
    image_path = os.path.join(path + '/Product Designs/')
    os.mkdir(path)
    os.mkdir(image_path)
    print("Directory '% s' created" % directory)

    list_image_locations = get_image_paths(sorted_list_product_ids)


    order_DF_1 = get_order_DF()
    order_DF_2 = get_order_items()
    order_DF_3 = get_product_ID_DataFrame()

    no_image = 'no_image.png'
    for image_name in list_image_locations:
        try:
            src_path = os.path.join('designs', image_name)
            dst_path = os.path.join(image_path , image_name)

            shutil.copy(src_path, dst_path)
        except:
            src_path = os.path.join('designs', no_image)
            dst_path = os.path.join(image_path , image_name)

            shutil.copy(src_path, dst_path)


    path_DF_1 = Path(path + '/OrderDetails.xlsx')
    order_DF_1.to_excel(path_DF_1, index=False)

    path_DF_2 = Path(path + '/OrderItemCount.xlsx')
    order_DF_2.to_excel(path_DF_2, index=False)

    path_DF_3 = Path(path + '/ProductQuantities.xlsx')
    order_DF_3.to_excel(path_DF_3, index=False)


def get_image_paths(list_product_ids):
    """
    Get a list of image paths for a list of product IDs.

    Args:
        list_product_ids (list): a list of product IDs

    Returns:
        list: a list of image paths for the product IDs
    """

    list_image_names = []

    for id in list_product_ids:

        if os.path.exists('designs/' + str(id) +'(1).png'):
            list_image_names.append(str(id)+'(1).png')
            list_image_names.append(str(id)+'(2).png')
        elif os.path.exists('designs/' + str(id) +'.png'):
            list_image_names.append(str(id)+'.png')
        else:
            list_image_names.append(str(id)+'.png')


    return list_image_names
