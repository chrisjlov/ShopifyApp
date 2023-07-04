import os
import pandas as pd

# Read in the csv file
df = pd.read_csv('product_data.csv')

# Create an empty list to store the data
data = []

# Iterate through the rows of the csv file
for index, row in df.iterrows():
  # Get the name and id of the current row
  name = row['name']
  id = row['id']

  # Check if the id is in the images folder
  if str(id) + '.png' in os.listdir('designs'):
    # If it is, add it to the data list
    data.append({'name': name, 'id': id})

# Create a new dataframe with the data list
new_df = pd.DataFrame(data)

new_df.to_csv("product_data_1.csv", index=False)
