from .landsat import Landsat

def main(start_date,end_date,file_path):

    baseUrl = "https://m2m.cr.usgs.gov/api/api/json/stable/"
    datasetName = "landsat_band_files_c2_l2"

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
        print("coordinate:",i+1,"out of",len(coordinates))
        landsat = Landsat(baseUrl,datasetName,coordinates[i][0],coordinates[i][1],start_date,end_date)
        retries = 1

        while landsat['error'][0] == 3 and retries<=3:
            retries+=1
            landsat = Landsat(baseUrl,datasetName,coordinates[i][0],coordinates[i][1],start_date,end_date) 

        if not landsat['success']:             
            print(landsat['error'][1])

start_date = '2024-01-01'
end_date = '2024-03-01'
file_path = 'co-ords.txt'
if __name__ == "__main__":
    main(start_date,end_date,file_path)