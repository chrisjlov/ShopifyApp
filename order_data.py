import pandas as pd

from shopify_orders import *


def count_order_items(DF):
    """
    Count the number of each type and size of item in the orders data.

    This function counts the number of each type and size of item in the orders data
    and stores the results in global variables.

    Args:
        DF: The dataframe containing the orders data.

    Returns:
        None
    """
    global orderListingDF
    orderListingDF = pd.DataFrame(columns=('Item','Small','Medium','Large','XLarge','XXLarge', 'XXXLarge', 'ToteCount'))

    hoodieS = 0
    hoodieM = 0
    hoodieL = 0
    hoodieXL = 0
    hoodieXXL = 0
    hoodieXXXL = 0

    crewneckS = 0
    crewneckM = 0
    crewneckL = 0
    crewneckXL = 0
    crewneckXXL = 0
    crewneckXXXL = 0

    NIKEcrewneckS = 0
    NIKEcrewneckM = 0
    NIKEcrewneckL = 0
    NIKEcrewneckXL = 0
    NIKEcrewneckXXL = 0
    NIKEcrewneckXXXL = 0

    teeS = 0
    teeM = 0
    teeL = 0
    teeXL = 0
    teeXXL = 0
    teeXXXL = 0

    NIKEteeS = 0
    NIKEteeM = 0
    NIKEteeL = 0
    NIKEteeXL = 0
    NIKEteeXXL = 0
    NIKEteeXXXL = 0

    toteNum = 0

    for item in DF['productName']:
        hoodie = 'HOODIE'
        crewneck= 'CREWNECK'
        tee = 'TEE'

        small = '- S'
        medium = '- M'
        large = '- L'
        xlarge = '- XL'
        xxlarge = '- XXL'
        xxxlarge = '- XXXL'

        tote = 'TOTE'


        productName = str(item)

        if 'NIKE' in productName:
            if crewneck in productName:
                if small in productName:
                    NIKEcrewneckS += 1
                if medium in productName:
                    NIKEcrewneckM += 1
                if large in productName:
                    NIKEcrewneckL += 1
                if xlarge in productName:
                    NIKEcrewneckXL += 1
                if xxlarge in productName:
                    NIKEcrewneckXXL += 1
                if xxxlarge in productName:
                    NIKEcrewneckXXXL += 1
            elif tee in productName:
                if small in productName:
                    NIKEteeS += 1
                if medium in productName:
                    NIKEteeM += 1
                if large in productName:
                    NIKEteeL += 1
                if xlarge in productName:
                    NIKEteeXL += 1
                if xxlarge in productName:
                    NIKEteeXXL += 1
                if xxxlarge in productName:
                    NIKEteeXXXL += 1
        else:
            if crewneck in productName:
                if small in productName:
                    crewneckS += 1
                if medium in productName:
                    crewneckM += 1
                if large in productName:
                    crewneckL += 1
                if xlarge in productName:
                    crewneckXL += 1
                if xxlarge in productName:
                    crewneckXXL += 1
                if xxxlarge in productName:
                    crewneckXXXL += 1
            elif tee in productName:
                if small in productName:
                    teeS += 1
                if medium in productName:
                    teeM += 1
                if large in productName:
                    teeL += 1
                if xlarge in productName:
                    teeXL += 1
                if xxlarge in productName:
                    teeXXL += 1
                if xxxlarge in productName:
                    teeXXXL += 1
            elif hoodie in productName:
                if small in productName:
                    hoodieS += 1
                if medium in productName:
                    hoodieM += 1
                if large in productName:
                    hoodieL += 1
                if xlarge in productName:
                    hoodieXL += 1
                if xxlarge in productName:
                    hoodieXXL += 1
                if xxxlarge in productName:
                    hoodieXXXL += 1
            elif tote in productName:
                toteNum+=1

    NIKEcrewRow = {'Item' : 'Nike Rework Crewneck', 'Small' : NIKEcrewneckS, 'Medium' : NIKEcrewneckM, 'Large' : NIKEcrewneckL, 'XLarge' : NIKEcrewneckXL, 'XXLarge' : NIKEcrewneckXXL, 'XXXLarge' : NIKEcrewneckXXXL}
    NIKEteeRow = {'Item' : 'Nike TEE', 'Small' : NIKEteeS, 'Medium' : NIKEteeM, 'Large' : NIKEteeL, 'XLarge' : NIKEteeXL, 'XXLarge' : NIKEteeXXL, 'XXXLarge' : NIKEteeXXXL}
    crewneckRow = {'Item' : 'Crewneck', 'Small' : crewneckS, 'Medium' : crewneckM, 'Large' : crewneckL, 'XLarge' : crewneckXL, 'XXLarge' : crewneckXXL, 'XXXLarge' : crewneckXXXL}
    teeRow = {'Item' : 'Tee', 'Small' : teeS, 'Medium' : teeM, 'Large' : teeL, 'XLarge' : teeXL, 'XXLarge' : teeXXL, 'XXXLarge' : teeXXXL}
    hoodieRow = {'Item' : 'Hoodie', 'Small' : hoodieS, 'Medium' : hoodieM, 'Large' : hoodieL, 'XLarge' : hoodieXL, 'XXLarge' : hoodieXXL, 'XXXLarge' : hoodieXXXL}
    toteRow = {'Item' : tote, 'ToteCount' : toteNum}

    DF1 = pd.DataFrame(NIKEcrewRow, index=[0])
    DF2 = pd.DataFrame(NIKEteeRow, index=[1])
    DF3 = pd.DataFrame(crewneckRow, index=[2])
    DF4 = pd.DataFrame(teeRow, index=[3])
    DF5 = pd.DataFrame(hoodieRow, index=[4])
    DF6 = pd.DataFrame(toteRow, index=[5])

    orderListingDF = pd.concat([DF1, DF2, DF3, DF4, DF5, DF6])
    return orderListingDF

def get_order_items():
    """
    Return the dataframe containing the counted items data.

    This function returns the global dataframe containing the counted items data.

    Returns:
        pandas.DataFrame: The dataframe containing the counted items data.
    """
    return orderListingDF
