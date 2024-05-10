from process import process
from find_files import find

file_paths = find()
print(file_paths)
for i in range(0,len(file_paths),2):
    process(file_paths[i], file_paths[i+1], 'NDWI', 0.05, False)
