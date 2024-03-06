import json
from landsatxplore.api import API
from landsatxplore.earthexplorer import EarthExplorer


# Initialize a new API instance and get an access key
api = API("MurtazaAliKhokhar", "fLZEwWdaE|e78_S")

# Search for Landsat TM scenes
scenes = api.search(
    dataset='landsat_ot_c2_l2',
    latitude=24.55317,
    longitude=67.53525,
    start_date='2024-02-01',
    end_date='2024-03-01',
    max_cloud_cover=10
)

print(f"{len(scenes)} scenes found.")

print(scenes)

# Process the result
for scene in scenes:
    print(scene['acquisition_date'].strftime('%Y-%m-%d'))
    # Write scene footprints to disk
    fname = f"{scene['landsat_product_id']}.geojson"
    with open(fname, "w") as f:
        json.dump(scene['spatial_coverage'].__geo_interface__, f)

print(scene)

api.logout()

ee = EarthExplorer('MurtazaAliKhokhar', 'fLZEwWdaE|e78_S')

# ee.download('LC08_L2SP_152043_20240215_20240223_02_T1', output_dir='./data')

ee.logout()
