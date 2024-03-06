import utils as ut
import datetime
import json
from tqdm import tqdm
import requests
import os
from landsatxplore.api import API
from landsatxplore.earthexplorer import EarthExplorer


def Landsat(baseUrl,datasetName):
    '''

    spatialFilter_mbr =  {'filterType' : "mbr",
                      'lowerLeft' : {'latitude' : 60, 'longitude' : -50},
                      'upperRight' : { 'latitude' : 65, 'longitude' : -45}}
    
    spatialFilter_geojson = {'filterType' : "geojson",
                             'geoJson': {
                                 'type': "polygon",
                                 'coordinates': [[
                                     [32.78,72.76],
                                     [32.80,75.23],
                                     [30.66,72.81],
                                     [30.68,75.22],
                                     [32.78,72.76]
                                 ]]
                             },
    }

    acquisitionFilter = {
        "start": "2020-01-01",
        "end": "2020-12-31"
    }

    returnMessage = {
        'succes':False,
        'message':""
    }
                     
    
    
    if token is None:
        returnMessage['message'] = "Token Generation Failed"
        return returnMessage
    else:
        dprint("Token Successfully Generated")

    datasets = api.datasetSearch(datasetName)
    datasetFound = False

    for dataset in datasets:
        if dataset['datasetAlias'] == datasetName:
            dprint("Found dataset:", dataset['datasetAlias'])
            datasetFound = True

    if not datasetFound:
        msg = "Dataset not found\n"
        msg += "Other Datasets found\n"
        for i in datasets:
            msg += i['datasetAlias'] + "\n"
        returnMessage['message'] = msg
        return returnMessage

    scenes = api.sceneSearch(1, 1, spatialFilter_geojson, acquisitionFilter)

    if scenes['recordsReturned'] == 0:
        returnMessage['message'] = "No scenes found"
        return returnMessage
    '''
    api = ut.utils(baseUrl,datasetName)
    token = api.generateKey("musutfa","Playstore123$")

    # Initialize a new API instance and get an access key
    xplorer = API("MurtazaAliKhokhar", "fLZEwWdaE|e78_S")

    # Search for Landsat TM scenes
    scenes = xplorer.search(
        dataset='landsat_ot_c2_l2',
        latitude=24.55317,
        longitude=67.53525,
        start_date='2024-02-01',
        end_date='2024-03-01',
        max_cloud_cover=10
    )

    print(f"{len(scenes)} scenes found.")

    # dprint("Scenes found: ", scenes['recordsReturned'])
    sceneIds = []
    band_names = ["_QA_PIXEL_TIF","_QA_RADSAT_TIF","_SR_B1_TIF","_SR_B2_TIF","_SR_B3_TIF","_SR_B4_TIF","_SR_B5_TIF","_SR_B6_TIF","_SR_B7_TIF"]
    for scene in scenes:
        # print(scene)
        for y in band_names:
            x = "L2SR_"+scene['display_id']+y
            # sceneIds.append(scene['display_id'])
            sceneIds.append(x)

    dprint("scene ids")
    print(sceneIds)

    downloadOptions = api.downloadOptions(sceneIds)
    # print(downloadOptions)

    if not downloadOptions:
        print("no")
    #     returnMessage['message'] = "No download options found"
    #     return returnMessage
    
    dprint("Download options found")

    downloads = []
    for product in downloadOptions:
        if product['available'] == True:
            downloads.append({
                "entityId": product['entityId'],
                "productId": product['id']
            })

    # if not downloads:
    #     returnMessage['message'] = "No products available to download right now"
    #     return returnMessage

    dprint("Products available to download: ", len(downloads))
    # print("here",downloads)
    requestedDownloads = len(downloads)
    # print("downloads",downloads)
    label = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    requestResults = api.downloadRequest(downloads, label)
    # if not requestResults['availableDownloads']:
    #     returnMessage['message'] = "No download options found"
    #     return returnMessage

    # print("Requested downloads: ", requestResults)

    downloadLinks = dict()
    print(len(requestResults['availableDownloads']))
    for download in requestResults['availableDownloads']:
        print(download)
        # name = download['url'].split('/')[-1].split('?')[0]
        id = download['downloadId']
        if id in downloadLinks:
            downloadLinks[id].append(download['url'])
        else:
            downloadLinks[id] = [download['url']]
        
    # print(downloadLinks)
    for i in downloadLinks:
        dprint("Download options for ",i)
        for idx,j in enumerate(downloadLinks[i]):
            dprint(str(idx+1)+")",j)

    for idx,i in enumerate(downloadLinks):
        if idx==0:
            url = downloadLinks[i][0]
            downloadFile(url,i)
    # returnMessage['succes'] = True
    # return returnMessage

def dprint(*args):
    print(*args)
    print("--------------------------")

def downloadFile(
        url, name, timeout=300, chunk_size=1024, skip=False, overwrite=False
    ):
    
        download_directory = "downloads/"

        if not os.path.exists(download_directory):
            os.makedirs(download_directory)

        output_file = os.path.join(download_directory, str(name))

        with requests.session() as session:
            response = session.get(url)
            if response.status_code == 200:
                with open(output_file, 'wb') as f:
                    f.write(response.content)
                print("File downloaded successfully.")
            else:
                print("Failed to download the file.")
        
