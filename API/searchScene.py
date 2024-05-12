from landsat import Landsat
import sys
import datetime
import shutil

def searchScene(file_path,cloud_cover,method='NDWI',start_date='',end_date='',download_all=False):

    baseUrl = "https://m2m.cr.usgs.gov/api/api/json/stable/"
    datasetName = "landsat_band_files_c2_l2"

    # if bands:
    #     if '-' in bands:
    #         bands = bands.split('-')
    #         bands = [str(i) for i in range(int(bands[0]),int(bands[1])+1)]
    #     elif ',' in bands:
    #         bands = bands.split(',')
    #     else:
    #         bands = [bands]

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

    # directory_to_delete = 'downloads'
    # try:
    #     shutil.rmtree(directory_to_delete)
    #     print("Directory", directory_to_delete, "successfully deleted.")
    # except FileNotFoundError:
    #     pass
    # except Exception as e:
    #     print("An error occurred:", e)

    for i in range(len(coordinates)):
        failed = []
        print("coordinate:",i+1,"out of",len(coordinates))
        landsat = Landsat(baseUrl,datasetName,coordinates[i][0],coordinates[i][1],start_date,end_date,download_all,cloud_cover,method)
        retries = 0

        while landsat['error'][0] is not None and retries<=3:
            retries+=1
            print("retrying...")
            landsat = Landsat(baseUrl,datasetName,coordinates[i][0],coordinates[i][1],start_date,end_date,download_all,cloud_cover,method) 

        if retries==4:
            print("Could not get data for coordinate:",i+1)
            failed.append(i+1)
            continue

        if not landsat['success']:             
            print(landsat['error'][1])

    if len(failed)>0:
        print("Failed coordinates:",failed)


if __name__ == "__main__":
    if len(sys.argv) > 6:
        print("Usage: python main.py [<file_path>] [<start_date>] [<end_date>]")
        sys.exit(1)

    # bands = sys.argv[1] if len(sys.argv) > 1 else '3,5,6,7'
    file_path = sys.argv[1] if len(sys.argv) > 1 else 'API/co-ords.txt'
    cloud_cover = sys.argv[2] if len(sys.argv) > 2 else 25
    start_date = sys.argv[3] if len(sys.argv) > 3 else datetime.date.today().strftime('%Y-%m-%d')
    end_date = sys.argv[4] if len(sys.argv) > 4 else ''
    download_all = sys.argv[5] if len(sys.argv) > 5 else False
    searchScene(file_path,cloud_cover,start_date=start_date,end_date=end_date,download_all=download_all)