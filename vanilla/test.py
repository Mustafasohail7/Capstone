from process import process
from find_files import find
from main_helper import *

file_paths = find()
file_paths.sort()
print("total iterations",len(file_paths))
# write_to_csv_header('output.csv',['Date','Net Change'])
terminated = 19
for i in range(terminated,len(file_paths)):
    print("iteration",i)
    process(file_paths[i-1], file_paths[i], 'NDWI', 0.05, False)
