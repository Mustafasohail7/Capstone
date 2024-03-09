from landsat import Landsat

def main():

    baseUrl = "https://m2m.cr.usgs.gov/api/api/json/stable/"
    datasetName = "landsat_band_files_c2_l2"
    # datasetName = "gls_all"

    # landsat = Landsat(baseUrl,datasetName)
    # if not landsat['success']:
    # # print("Error")
    #     print(landsat['message'])
    file_path = 'co-ords.txt'
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
        landsat = Landsat(baseUrl,datasetName,coordinates[i][0],coordinates[i][1])
        retries = 1

        while landsat['error'][0] == 3 and retries<=3:
            retries+=1
            landsat = Landsat(baseUrl,datasetName,coordinates[i][0],coordinates[i][1]) 

        if not landsat['success']:             
            print(landsat['message'])

main()