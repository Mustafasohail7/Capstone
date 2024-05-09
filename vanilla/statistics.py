import pandas as pd
import numpy as np

# Load the CSV file into a DataFrame
file_path = "output.csv"
data = pd.read_csv(file_path,usecols=[1])

# Explore the data (optional)
print(data.head())  # Display the first few rows of the DataFrame

# Perform basic statistical analysis
mean = data.mean()
std_dev = data.std()
distribution = data.describe()  # Summary statistics

# Display the results
print("Mean:", mean)
print("Standard Deviation:", std_dev)
print("Distribution:", distribution)
