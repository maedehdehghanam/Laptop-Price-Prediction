import pandas as pd
import ast

# Read the text file
with open('data_hp.txt', 'r') as file:
    lines = file.readlines()
with open('get_link_hp.txt', 'r') as file:
    links = file.readlines()

dataset = []
# Process each line
for line in lines:
    price, features = line.split('{', 1)
    features = '{' + features  # Add back the curly brace
    features_dict = ast.literal_eval(features)  # Convert string to dictionary
    features_dict['price'] = int(price)  # Add the price to the dictionary
    dataset.append(features_dict)

# Create DataFrame
df = pd.DataFrame(dataset)

# Rearrange columns to have 'price' as the first column
cols = ['price'] + [col for col in df.columns if col != 'price']
df = df[cols]


# Fill missing values with NaN
df['cpu'] = df['cpu'].fillna('Core i3')
df['screen_size'] = df['screen_size'].fillna('15')
df['graphic_ram'] = df['graphic_ram'].fillna('0')
df['hdd'] = df['hdd'].fillna('0')
df['ssd'] = df['ssd'].fillna('0')
df = df.fillna('0')

# Replace 0 values in a specific column with 'unified'
column_name = 'graphic_ram'  # Replace with the actual column name
df[column_name] = df[column_name].replace('unified', '0')
df[column_name] = df[column_name].str.replace(' mb', '')
df[column_name] = df[column_name].str.replace(' gb', '000').astype(int)

# Remove 'gb' part and convert the column to integers
column_name = 'hdd'  # Replace with the actual column name
df[column_name] = df[column_name].str.replace(' gb', '')
df[column_name] = df[column_name].str.replace(' tb', '000').astype(int)

column_name = 'ssd'  # Replace with the actual column name
df[column_name] = df[column_name].str.replace(' gb', '')
df[column_name] = df[column_name].str.replace(' tb', '000').astype(int)

column_name = 'ram'  # Replace with the actual column name
df[column_name] = df[column_name].str.replace(' mb', '')
df[column_name] = df[column_name].str.replace(' gb', '000').astype(int)

column_name = 'screen_size'  # Replace with the actual column name
df[column_name] = df[column_name].str.replace(' inch', '').astype(float)

df['company'] = 'hp'
df['links'] = [link.strip() for link in links]

zero_counts = (df == '0').sum(axis=1)

# Remove lines with more than three zeros
df = df[zero_counts <= 3]
# Print the resulting DataFrame
print(df.head())

# Save the updated DataFrame as a new CSV file
df.to_csv('hp_dataset.csv', index=False)
