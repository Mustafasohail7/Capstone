from landsat import Landsat

def main():

    baseUrl = "https://m2m.cr.usgs.gov/api/api/json/stable/"
    datasetName = "landsat_band_files_c2_l2"
    # datasetName = "gls_all"

    landsat = Landsat(baseUrl,datasetName)
    if not landsat['succes']:
    # print("Error")
        print(landsat['message'])

main()