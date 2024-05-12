import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Read data from CSV file
df = pd.read_csv('output.csv')

# Step 2: Convert 'Date' column to datetime format
df['Date'] = pd.to_datetime(df['Date'], format='%Y%m%d')

# Step 3: Plot the data
plt.figure(figsize=(10, 6))
plt.plot(df['Date'], df['Net Change'], marker='o', linestyle='-')

# Step 4: Add labels and title
plt.xlabel('Date')
plt.ylabel('Net Change')
plt.title('Net Change Across Dates')
plt.grid(True)

# Step 5: Rotate x-axis labels for better readability
plt.xticks(rotation=45)

# Step 6: Show plot
plt.tight_layout()
plt.show()
