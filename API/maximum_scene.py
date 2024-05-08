from utils import utils 
from landsatxplore.api import API

coordinates = []
file_path = 'API/co-ords.txt'
with open(file_path, 'r') as file:
    for line in file:
        parts = line.strip().split(',')
        if len(parts) == 2:  # Making sure there are exactly two elements
            try:
                num1, num2 = float(parts[0]), float(parts[1])
                coordinates.append((num1, num2))
            except ValueError:  # In case the conversion to float fails
                print(f"Could not convert line to floats: {line.strip()}")

baseUrl = "https://m2m.cr.usgs.gov/api/api/json/stable/"
datasetName = "landsat_band_files_c2_l2"
api = utils(baseUrl,datasetName)
api.generateKey("musutfa","Playstore123$")

# Initialize a new API instance and get an access key
xplorer = API("MurtazaAliKhokhar", "fLZEwWdaE|e78_S")
num_scenes = []
for i in range(len(coordinates)):
    scenes = xplorer.search(
        dataset='landsat_ot_c2_l2',
        latitude=coordinates[i][0],
        longitude=coordinates[i][1],
        start_date='2023-01-01',
        end_date='2023-12-31',
        max_cloud_cover=25
    )
    num_scenes.append(len(scenes))

srted = num_scenes.copy()
print(num_scenes)

