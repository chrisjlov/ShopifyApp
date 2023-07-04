## ---------------------------
##
## Script name: main.py
##
## Purpose of script: Main rountine to import order data from shopify
##
## Author: Chris Lovett
##
## Date Created: 2022-10-30
##
## Copyright (c) Chris Lovett, 2022
##
## ---------------------------
from tkinter import *
from PIL import Image, ImageTk
from tkinter import filedialog
from tkcalendar import *
from psd_tools import PSDImage

import tkinter as tk

from shopify_orders import *
from show_orders import *
from save_images import *
from order_data import *
from all_products import *

class Application:
    def __init__(self, window):
        """
        This is the main class for the SHOPIFY application. It creates the main window and sets up the header and main frame for the application. It also initializes the different pages (or frames) that the application can display.

        Parameters:
        window (Tk object): The main window of the application.

        """

        self.window = window
        self.window.title('STORE NAME')
        self.window.minsize(height=900,width=1400)

        self.window.config(background='#eff5f6')

        #Application Icon
        icon = PhotoImage(file='YOUR ICON IMAGE PATH')
        self.window.iconphoto(True, icon)

        #Main frame for application
        container = Frame(window, height=400, width=600, bg='#b7b7b7')
        container.pack(side='bottom',fill='both', expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        #Header frame
        global header
        header = Frame(window,height=60, width=1366, bg ='#5c5c5c')
        header.pack(side='top',fill='both', expand=True)

        header.grid_rowconfigure(0, weight=1)
        header.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (mainPage, orderPage, updatePage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(mainPage)

    def show_frame(self, cont):
        """
        This method raises the specified frame to the top of the window stack.

        Parameters:
        cont (Frame object): The frame to be displayed.
        """
        frame = self.frames[cont]
        # raises the current frame to the top
        frame.tkraise()
        clear_orders(order_frame)

class mainPage(Frame):
    def __init__(self, parent, controller):
        """
        This class represents the main page of the SHOPIFY Archive application. It contains buttons for navigating to the other pages of the application.

        Parameters:
        parent (Frame object): The parent frame for this page.
        controller (Application object): The main Application object for the application.
        """
        Frame.__init__(self, parent)
        label = Label(self, text="Main Page", font=("Arial", 25))
        label.pack(padx=10, pady=10)

        #Homepage Button
        self.logo_image = Image.open('YOUR LOGO PATH')
        photo = ImageTk.PhotoImage(self.logo_image)
        self.logo = Label(header, image=photo, bg='#E3E5E0')
        self.logo.image = photo

        homepage_button = Button(
            header,
            text="",
            image=photo,
            command=lambda: controller.show_frame(mainPage),
        )

        # We use the switch_window_button in order to call the show_frame() method as a lambda function
        switch_window_button = Button(
            self,
            text="Orders",
            command=lambda: controller.show_frame(orderPage),
        )

        upload_PNG = Button(
            self,
            text="Update images",
            command=lambda:controller.show_frame(updatePage),
        )

        homepage_button.pack(side="top")
        switch_window_button.pack(side="top")
        upload_PNG.pack(side="top")



class orderPage(Frame):
    def __init__(self, parent, controller):
        """
        This class represents the order page of the SHOPIFY Archive application. It contains a form for the user to input a date range and buttons to submit the date range and view today's orders. It also has a button to save the orders to a folder.

        Parameters:
        parent (Frame object): The parent frame for this page.
        controller (Application object): The main Application object for the application.
        """

        Frame.__init__(self, parent)

        # create canvas for scrollable window
        canvas = Canvas(self)
        canvas.grid(row=1,column=0, columnspan=2)

        # Frame for Orders
        global order_frame
        order_frame = Frame(self, height=700, width=1300, bg='#808080')
        order_frame.grid(row=1, column=4, sticky = 'ns')

        self.save_directory_button = tk.Button(canvas, text="Save Directory",font=('TKDefaultFont', 10, 'bold'),
                                relief=RAISED, command=choose_directory, bg = "gray80")
        self.save_directory_button.grid(row=15, column = 0, columnspan=8, sticky = 'EW')

        # Proposal Date
        self.start_date_label = Label(canvas, text="Start Date:",font=('TKDefaultFont', 8, 'bold'))
        self.start_date_label.grid(row=21, column=0, sticky=W)

        self.end_date_label = Label(canvas, text="End Date:",font=('TKDefaultFont', 8, 'bold'))
        self.end_date_label.grid(row=25, column=0, sticky=W)

        self.date_start_input = DateEntry(canvas, width = 25, background = 'LightCyan3',
                                             foreground ='white',borderwidth=2)
        self.date_start_input.grid(row=21, column=1,sticky=E)
        self.date_start_input.delete(0,"end")

        self.date_end_input = DateEntry(canvas, width = 25, background = 'LightCyan3',
                                             foreground ='white',borderwidth=2)
        self.date_end_input.grid(row=25, column=1,sticky=E)
        self.date_end_input.delete(0,"end")


        # SUBMIT INFORMATION
        self.button = tk.Button(canvas, text="Submit Dates",font=('TKDefaultFont', 10, 'bold'),
                                relief=RAISED, command = self.store_user_inputs, bg = "gray80")
        self.button.grid(row=27, column = 0, columnspan=8, sticky = 'EW')

         # Today's Date
        self.todayButton = tk.Button(canvas, text="Today\'s Orders",font=('TKDefaultFont', 10, 'bold'),
                                relief=RAISED, command=lambda:get_todays_orders(order_frame), bg = "gray80")
        self.todayButton.grid(row=45, column = 0, columnspan=8, sticky = 'EW')

        # Save Orders
        self.saveButton = tk.Button(canvas, text="Save Orders to Folder",font=('TKDefaultFont', 10, 'bold'),
                                relief=RAISED, command=lambda:save_to_folder(params[0],params[1], folder_selected, sorted_list_product_ids), bg = "gray80")
        self.saveButton.grid(row=50, column = 0, columnspan=8, sticky = 'EW')

        # Get all Products Details
        self.saveButton = tk.Button(canvas, text="Get all Product Details",font=('TKDefaultFont', 10, 'bold'),
                                relief=RAISED, command=lambda:get_all_products_details(folder_selected, False), bg = "gray80")
        self.saveButton.grid(row=55, column = 0, columnspan=8, sticky = 'EW')


    # STORE USER INPUT
    def store_user_inputs(self):
        """
        Retrieve and process orders data based on user input dates.

        This function retrieves the start and end dates specified by the user and uses
        them to retrieve and process orders data. The resulting data is then displayed
        to the user.

        Args:
            self: The object instance.

        Returns:
            None
        """

        date_start_input = self.date_start_input.get_date()
        date_end_input = self.date_end_input.get_date()

        global params, sorted_list_product_ids
        params = [date_start_input,date_end_input]
        two_dates_orders_JSON_data, order_count = get_orders_two_dates(date_start_input,date_end_input)
        two_dates_orders_DF, list_product_ids = sort_orders(two_dates_orders_JSON_data)
        print(order_count)
        amount_of_products = len(list_product_ids)
        sorted_list_product_ids = sort_product_ids(list_product_ids, False)
        count_order_items(two_dates_orders_DF)

        clear_orders(order_frame)


        navigation_frame = Frame(order_frame)
        navigation_frame.grid(row=55, column = 0, columnspan=8, sticky = 'EW')

        page_label = None

        show_orders(two_dates_orders_DF,order_frame, order_count, amount_of_products,1, None, navigation_frame, page_label)



global folder_selected

def choose_directory():
    """
    This function allows the user to select a directory to save the orders to.

    Returns:
    None
    """

    global folder_selected
    root = Tk()
    root.withdraw()
    folder_selected = filedialog.askdirectory()

def get_todays_orders(frame):
    """
    Retrieve and display today's orders data.

    This function retrieves and processes today's orders data and displays it to the user.

    Args:
        frame: The parent frame where the orders data will be displayed.

    Returns:
        None
    """
    today_orders_JSON_data, order_count = get_orders_today()
    today = date.today()
    global params,sorted_list_product_ids
    params = [today,today]
    today_orders_DF, list_product_ids = sort_orders(today_orders_JSON_data)

    amount_of_products = len(list_product_ids)
    sorted_list_product_ids = sort_product_ids(list_product_ids, False)

    count_order_items(today_orders_DF)

    clear_orders(order_frame)

    navigation_frame = Frame(order_frame)
    navigation_frame.grid(row=55, column = 0, columnspan=8, sticky = 'EW')

    page_label = None

    show_orders(today_orders_DF,order_frame, order_count, amount_of_products,1, None, navigation_frame, page_label)





class updatePage(Frame):
    def __init__(self, parent, controller):
        """
        This class represents the update page where the user can upload and view files.

        Parameters:
        parent (Frame object): The parent frame for this update page.
        controller (Application object): The Application object that controls the flow between pages.
        """

        Frame.__init__(self, parent)
        label1 = Label(self, text="Update Page", font=("Arial", 25))
        label1.pack(padx=10, pady=10)

        #upload png to design folder
        upload = Button(self,text='Upload File', width=20,command = lambda:upload_file()).pack()

        #view/edit pngs in design folder
        view = Button(self,text='View Files', width=20,command = lambda:view_files()).pack()

        def upload_file():
            """
            This function allows the user to select a file to upload to the 'designs' folder.

            Returns:
            None
            """

            global img
            f_types = [('PNG Files', '*.png')]
            filepath = filedialog.askopenfilename(filetypes=f_types)
            img = Image.open(filepath)
            filename = str(os.path.basename(filepath))
            img.save('designs/'+filename)

        def view_files():
            """
            This function opens the 'designs' folder in the user's file explorer.

            Returns:
            None
            """

            path = "designs/"
            path = os.path.realpath(path)
            os.startfile(path)


def win():
    """
    This function creates the main window and runs the application.

    Returns:
    None
    """

    window = Tk()
    Application(window)
    window.mainloop()


if __name__ == '__main__':
    win()


