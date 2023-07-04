# ---------------------------
##
# Script name: show_orders.py
##
# Purpose of script: Displays orders in application
##
# Author: Chris Lovett
##
# Date Created: 2022-10-30
##
# Copyright (c) Chris Lovett, 2022
##
# ---------------------------

import os
import math
import pandas as pd

from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk

from shopify_orders import *

global list_image_names, list_image_locations

def open_50_images(list_product_ids):
    """
    Load and resize a set of product images.

    This function loads and resizes a set of product images and stores them in global
    variables. The images are specified by their product IDs, which are passed as a
    list. The function also stores the names and locations of the images, as well as
    the dimensions of the original images. If an image with a given product ID is not
    found, a placeholder "no image" image is used instead.

    Args:
        list_product_ids (list): The list of product IDs.

    Returns:
        tuple: A tuple containing the resized images and the dimensions of the original
            images.
    """
    global list_image_names, list_image_locations
    list_images_ordered = []
    list_images_dimensions = []

    list_image_locations = []
    list_image_names = []

    for id in list_product_ids:
        try:
            list_multi_images = []
            list_multi_image_dimensions = []

            product_id_1 = str(id)+'(1).png'
            with Image.open('designs/' + product_id_1) as image_of_order:
                locationimage_1 = image_of_order
                list_image_locations.append(locationimage_1)

                resized = image_of_order.resize(
                    (150, 120), Image.Resampling.LANCZOS)
                list_multi_image_dimensions.append(image_of_order.size)
                image_ordered = ImageTk.PhotoImage(resized)
                list_multi_images.append(image_ordered)

            list_image_names.append(product_id_1)

            product_id_2 = str(id)+'(2).png'
            with Image.open('designs/' + product_id_2) as image_of_order:
                locationimage_2 = image_of_order
                list_image_locations.append(locationimage_2)

                resized = image_of_order.resize(
                    (150, 120), Image.Resampling.LANCZOS)
                list_multi_image_dimensions.append(image_of_order.size)
                image_ordered = ImageTk.PhotoImage(resized)
                list_multi_images.append(image_ordered)

            list_image_names.append(product_id_2)

            list_images_dimensions.append(list_multi_image_dimensions)
            list_images_ordered.append(list_multi_images)
        except:
            product_id = str(id)+'.png'
            if os.path.exists('designs/' + product_id):
                with Image.open('designs/' + product_id) as image_of_order:
                    image_location = image_of_order
                    list_image_locations.append(image_location)

                    resized = image_of_order.resize(
                        (150, 120), Image.Resampling.LANCZOS)
                    list_images_dimensions.append(image_of_order.size)
                    image_ordered = ImageTk.PhotoImage(resized)
                    list_images_ordered.append(image_ordered)

                list_image_names.append(product_id)

            else:
                with Image.open('designs/no_image.png') as image_of_order:
                    image_location = image_of_order
                    list_image_locations.append(image_location)
                    resized = image_of_order.resize(
                        (150, 120), Image.Resampling.LANCZOS)
                    list_images_dimensions.append(
                        "No image dimensions available")
                    image_ordered = ImageTk.PhotoImage(resized)
                    list_images_ordered.append(image_ordered)

                list_image_names.append('no_image.png')

    list_image_names, list_duplicateIndexes = sort_product_ids(
        list_image_names, True)

    for indx in sorted(list_duplicateIndexes, reverse=True):
        list_image_locations.pop(indx)

    return list_images_ordered, list_images_dimensions





def show_orders(order_DF, win, order_count, amount_of_products, current_page, current_frame, navbar_made, page_label):
    """
    Display a list of orders in a GUI window. The orders are displayed in pages, with 50 orders per page. The user can
    navigate through the pages using buttons.

    Args:
        order_DF (pandas.DataFrame): a dataframe containing the orders to be displayed
        win (tkinter.Tk): a tkinter window object
        order_count (int): the total number of orders
        amount_of_products (int): the total number of products in the orders
        current_page (int): the current page number to be displayed
        current_frame (tkinter.Frame): a tkinter frame object representing the current frame in the window
        navbar_made (tkinter.Frame): a tkinter frame object representing a navigation bar (if it has already been made)
        page_label (tkinter.Label): a tkinter label object used to display the current page number

    Returns:
        None
    """

    if navbar_made is not None:
        # Destroy the current navigation bar
        navbar_made.destroy()

    # Create a new navigation bar
    navbar = Frame(win)
    navbar.grid(row=55, column = 0, columnspan=8, sticky = 'EW')

    # Update the navbar_made argument with the current navbar variable
    navbar_made = navbar

    global page

    page = current_page

    # Calculate the number of pages needed to display all orders
    num_pages = math.ceil(len(order_DF) / 50)

    # Slice the dataframe to get the orders in the current page
    page_df = order_DF.iloc[(page - 1) * 50: page * 50]

    #Gets rid of prevoius page number label
    if page_label is not None:
        page_label.destroy()

    # Create a label to display the page number
    page_label = Label(navbar, text="Page {} of {}".format(page, num_pages))
    page_label.pack(side=RIGHT)


    wrapper = LabelFrame(win)
    canvas = Canvas(wrapper, height=700, width=1300, bg='#808080')

    yscroll = ttk.Scrollbar(wrapper, orient='vertical', command=canvas.yview)
    yscroll.pack(side=RIGHT, fill='y')

    xscroll = ttk.Scrollbar(wrapper, orient='horizontal', command=canvas.xview)
    xscroll.pack(side=BOTTOM, fill='x')

    canvas.configure(yscrollcommand=yscroll.set)
    canvas.configure(xscrollcommand=xscroll.set)

    def _on_mousewheel(event):
        """
        Scroll the canvas up or down when mouse wheel is used

        Args:
            event (tkinter.Event): Mouse wheel event

        Returns:
            None
        """
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    canvas.bind('<Configure>', lambda e: canvas.configure(
        scrollregion=canvas.bbox('all')))
    canvas.bind_all("<MouseWheel>", _on_mousewheel)
    canvas.pack(side=LEFT, fill='both', expand='yes')

    myframe = Frame(canvas)
    canvas.create_window((0, 0), window=myframe, anchor='nw')

    # Replace the current frame with the new frame
    if current_frame is not None:
        current_frame.pack_forget()
    wrapper.grid(row=0, column=0, sticky='nsew')
    current_frame = wrapper

    # Get the product IDs for the orders in the current page
    page_product_ids = page_df['productID'].tolist()

    # Open the images for the product IDs in the current page
    list_images, list_image_dimensions = open_50_images(page_product_ids)


    amount_of_orders = str(order_count)
    amount_of_products = str(amount_of_products)

    # Label for showing how many orders and products ordered there are
    Label(myframe, text="Amount of Orders: " + amount_of_orders, justify=LEFT,
        anchor="w", font=('TKDefaultFont', 10, 'bold')).grid(sticky=W)
    Label(myframe, text="Amount of Products Ordered: " + amount_of_products,
        justify=LEFT, anchor="w", font=('TKDefaultFont', 10, 'bold')).grid(sticky=W)



    def go_first_page():
        """Go to the first page"""
        global page
        global page_product_ids
        page = 1
        page_df = order_DF.iloc[(page - 1) * 50: page * 50]
        page_product_ids = page_df['productID'].tolist()
        show_orders(order_DF, win, order_count, amount_of_products, page, current_frame, navbar_made, page_label)


    def go_prev_page():
        """Go to the previous page"""
        global page
        global page_product_ids

        if page > 1:
            page -= 1
            page_df = order_DF.iloc[(page - 1) * 50: page * 50]
            page_product_ids = page_df['productID'].tolist()
            show_orders(order_DF, win, order_count, amount_of_products, page, current_frame, navbar_made, page_label)

    def go_next_page():
        """Go to the next page"""
        global page
        global page_product_ids
        if page < num_pages:
            page += 1
            page_df = order_DF.iloc[(page - 1) * 50: page * 50]
            page_product_ids = page_df['productID'].tolist()
            show_orders(order_DF, win, order_count, amount_of_products, page, current_frame, navbar_made, page_label)

    def go_last_page():
        """Go to the last page"""
        global page
        global page_product_ids
        page = num_pages
        page_df = order_DF.iloc[(page - 1) * 50: page * 50]
        page_product_ids = page_df['productID'].tolist()
        show_orders(order_DF, win, order_count, amount_of_products, page, current_frame, navbar_made, page_label)

    # Create the navigation buttons
    first_button = Button(navbar, text="<<", command=go_first_page)
    prev_button = Button(navbar, text="<", command=go_prev_page)
    next_button = Button(navbar, text=">", command=go_next_page)
    last_button = Button(navbar, text=">>", command=go_last_page)

    # Pack the navigation buttons
    first_button.pack(side=LEFT)
    prev_button.pack(side=LEFT)
    next_button.pack(side=LEFT)
    last_button.pack(side=LEFT)

    page_df = page_df.reset_index(drop=True)


    for i in range(len(page_df)):
        if isinstance(list_images[i], list):
            details =  'PRODUCT_ID: ' + str(page_df.loc[i]['productID']) + '\n' + 'ORDER_NUMBER: ' + str(page_df.loc[i]['orderNumber']) + '\n' + 'PRODUCT_NAME: ' + str(
                page_df.loc[i]['productName']) + '\n' + 'SIZE: ' + str(page_df.loc[i]['size']) + '\n' + 'IMAGE_DIMENSIONS: ' + str(list_image_dimensions[i])

            image_1 = list_images[i][0]
            image_2 = list_images[i][1]
            label_1 = Label(myframe, text=details,
                            image=image_1, justify=LEFT, anchor="w")

            label_1.grid(sticky=W)
            label_1["compound"] = LEFT
            label_1.image = image_1

            label_2 = Label(myframe, image=image_2, justify=LEFT, anchor="w")

            label_2.grid(sticky=W)
            label_2["compound"] =LEFT
            label_2.image = image_2
        else:
            details = 'PRODUCT_ID: ' + str(page_df.loc[i]['productID']) + '\n' + 'ORDER_NUMBER: ' + str(page_df.loc[i]['orderNumber']) + '\n' + 'PRODUCT_NAME: ' + str(
                page_df.loc[i]['productName']) + '\n' + 'SIZE: ' + str(page_df.loc[i]['size']) + '\n' + 'IMAGE_DIMENSIONS: ' + str(list_image_dimensions[i])

            label_1 = Label(myframe, text=details, image=list_images[i],
                            justify=LEFT, anchor="w")

            label_1.grid(sticky=W)
            label_1["compound"] = LEFT
            label_1.image = list_images[i]

    current_frame = wrapper



def clear_orders(frame):
    """
    Clear widgets from a frame

    Args:
        frame (tkinter.Frame): Frame containing widgets to be removed

    Returns:
        None
    """
    for widgets in frame.winfo_children():
        widgets.destroy()


# def get_list_image_path():
#     """
#     Get list of image file paths

#     Returns:
#         list: List of image file paths
#     """
#     list_image_locations
#     return list_image_locations


# def get_list_image_ids():
#     """
#     Get list of image file names

#     Returns:
#         list: List of image file names
#     """
#     return list_image_names

