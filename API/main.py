from landsat import Landsat
import sys

def clear_output():
    # ANSI escape code to clear the screen
    sys.stdout.write('\033[2J\033[H')
    sys.stdout.flush()

def main(start_date,end_date,file_path,bands):

    baseUrl = "https://m2m.cr.usgs.gov/api/api/json/stable/"
    datasetName = "landsat_band_files_c2_l2"

    if bands:
        if '-' in bands:
            bands = bands.split('-')
            bands = [str(i) for i in range(int(bands[0]),int(bands[1])+1)]
        elif ',' in bands:
            bands = bands.split(',')
        else:
            bands = [bands]

    coordinates = []
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            if len(parts) == 2:  # Making sure there are exactly two elements
                try:
                    num1, num2 = float(parts[0]), float(parts[1])
                    coordinates.append((num1, num2))
                except ValueError:  # In case the conversion to float fails
                    print(f"Could not convert line to floats: {line.strip()}")
    #print(coordinates)

    for i in range(len(coordinates)):
        failed = []
        print("coordinate:",i+1,"out of",len(coordinates))
        landsat = Landsat(baseUrl,datasetName,coordinates[i][0],coordinates[i][1],start_date,end_date,bands)
        retries = 0

        while landsat['error'][0] is not None and retries<=3:
            retries+=1
            print("retrying...")
            landsat = Landsat(baseUrl,datasetName,coordinates[i][0],coordinates[i][1],start_date,end_date,bands) 

        if retries==4:
            print("Could not get data for coordinate:",i+1)
            failed.append(i+1)
            continue

        if not landsat['success']:             
            print(landsat['error'][1])
        
        clear_output()

    if len(failed)>0:
        print("Failed coordinates:",failed)


if __name__ == "__main__":
    if len(sys.argv) > 5:
        print("Usage: python main.py [<start_date>] [<end_date>] [<file_path>] [<bands>]")
        sys.exit(1)

    bands = sys.argv[1] if len(sys.argv) > 1 else '3,5,6,7'
    start_date = sys.argv[2] if len(sys.argv) > 2 else '2024-01-01'
    end_date = sys.argv[3] if len(sys.argv) > 3 else '2024-03-01'
    file_path = sys.argv[4] if len(sys.argv) > 4 else 'API/co-ords.txt'
    main(start_date,end_date,file_path,bands)