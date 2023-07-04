from all_products import get_all_products_details
from get_order_data import get_order_data

"""
Test Retrieval of Order and Product Data
Also tests API version is up to date
"""

product_test = get_all_products_details(None, True)
print(product_test)

#start date test
start_date = '2023-07-01 23:00:00'
#end date test
end_date = '2023-07-02 22:59:59'

order_test = get_order_data(start_date, end_date, True)
print(order_test)
