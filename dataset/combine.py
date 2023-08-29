import pandas as pd
import glob

# Get a list of all CSV files in the current directory
csv_files = glob.glob("*_dataset.csv")

# Create an empty list to store the data frames
dfs = []

# Read each CSV file and append its data frame to the list
for file in csv_files:
    df = pd.read_csv(file)
    dfs.append(df)

# Concatenate all the data frames into a single data frame
combined_df = pd.concat(dfs)

# Shuffle the rows of the combined data frame
shuffled_df = combined_df.sample(frac=1).reset_index(drop=True)

# Save the shuffled data frame to a new CSV file
shuffled_df.to_csv("combined_and_shuffled.csv", index=False)

print("Combined and shuffled CSV file created successfully.")
