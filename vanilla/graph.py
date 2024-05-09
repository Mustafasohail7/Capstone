import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file into a DataFrame
file_path = "output.csv"
data = pd.read_csv(file_path)

# Plot the data
plt.figure(figsize=(10, 6))
plt.plot(data['Date'], data['Water Volume'], marker='o', linestyle='-')
plt.title('Change in Water Volume Across 25 Days')
plt.xlabel('Date')
plt.ylabel('Water Volume')
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()

# Calculate the average change across each value
volume_changes = data['Water Volume'].diff()  # Calculate the change in volume between consecutive days
average_change = volume_changes.mean()
print("Average change in water volume across each value:", average_change)
