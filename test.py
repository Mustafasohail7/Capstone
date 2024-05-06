import pickle
import os

# Assuming you have saved the centerlines as 'centerlines.pkl'
input_path = "centerlines.pkl"

# Load the centerlines array from the pickle file
with open(input_path, 'rb') as f:
    centerlines = pickle.load(f)

a = 0
for i in centerlines:
    for j in i:
        if j!=False:
            a+=1

print(a)
