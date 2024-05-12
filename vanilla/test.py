from process import process
from find_files import find
from main_helper import *
import sys

def main(n):
    file_paths = find()
    file_paths.sort()
    print("total iterations",len(file_paths))
    # write_to_csv_header('output.csv',['Date','Net Change'])
    terminated = n
    for i in range(terminated,len(file_paths)):
        print("iteration",i)
        process(file_paths[i-1], file_paths[i], 'NDWI', 0.05, False)
        print("done")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Invalid number of arguments. Please provide 1 argument: number of iterations.")
        sys.exit(1)
    n = int(sys.argv[1])
    main(n)
