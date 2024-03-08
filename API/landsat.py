import utils as ut
import datetime
import requests
import os
import datetime
from landsatxplore.api import API

download_directory = ("downloads/{image_name}")

def Landsat(baseUrl,datasetName,lat,lon):

    returnMessage = {
        'success':False,
        'message':""
    }

    api = ut.utils(baseUrl,datasetName)
    api.generateKey("musutfa","Playstore123$")

    # Initialize a new API instance and get an access key
    xplorer = API("MurtazaAliKhokhar", "fLZEwWdaE|e78_S")

    # Search for Landsat TM scenes3 
    scenes = xplorer.search(
        dataset='landsat_ot_c2_l2',
        latitude=lat,
        longitude=lon,
        start_date='2024-01-01',
        end_date='2024-03-01',
        max_cloud_cover=10
    )

    print(f"{len(scenes)} scenes found.")
    
    latest_scene = None
    latest_date = datetime.datetime.min  # Set to the earliest possible date for comparison

    for scene in scenes:
        if scene['date_product_generated'] > latest_date:
            latest_date = scene['date_product_generated']
            latest_scene = scene
    print(latest_date)
    # dprint("Scenes found: ", scenes['recordsReturned'])
    sceneIds = []
    band_names = ["_SR_B7_TIF"]
    #band_names = ["_QA_PIXEL_TIF","_QA_RADSAT_TIF","_SR_B1_TIF","_SR_B2_TIF","_SR_B3_TIF","_SR_B4_TIF","_SR_B5_TIF","_SR_B6_TIF","_SR_B7_TIF"]
    for band in band_names:
        scene_name = "L2SR_"+latest_scene['display_id']+band
        # sceneIds.append(scene['display_id'])
        sceneIds.append(scene_name)

    # dprint("scene ids")
    # print(sceneIds)

    downloadOptions = api.downloadOptions(sceneIds)

    if not downloadOptions:
        returnMessage['message'] = "No download options found"
        return returnMessage
    
    
    dprint("Download options found")

    downloads = []
    for product in downloadOptions:
        if product['available'] == True:
            downloads.append({
                "entityId": product['entityId'],
                "productId": product['id']
            })

    if not downloads:
        returnMessage['message'] = "No products available to download right now"
        return returnMessage

    dprint("Products available to download: ", len(downloads))

    label = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    requestResults = api.downloadRequest(downloads, label)
    if not requestResults['availableDownloads']:
        returnMessage['message'] = "No download options found"
        return returnMessage

    # print(len(sceneIds))
    # print(len(int(requestResults['availableDownloads'])/2))

    if len(sceneIds) == int(len(requestResults['availableDownloads'])/2):
        print("mappable")

    newResults = []
    for idx,download in enumerate(requestResults['availableDownloads']):
        newObj = {**download, 'name': sceneIds[idx//2]}
        newResults.append(newObj)

    # for i in newResults:
    #     print(i)

    downloadLinks = dict()
    for download in newResults:
        name = download['name']
        if name in downloadLinks:
            downloadLinks[name].append(download['url'])
        else:
            downloadLinks[name] = [download['url']]
        
    # print(downloadLinks)
    for i in downloadLinks:
        downloaded = False
        for j in downloadLinks[i]:
            url = j
            if not downloaded:
                downloaded = downloadFile(url,i)

    returnMessage['succes'] = True
    return returnMessage

def dprint(*args):
    print(*args)
    print("--------------------------")

def downloadFile(url, name):
    
        n = name.split('_')
        short_name = '_'.join(n[1:7 + 1])

        dir = download_directory.format(image_name=short_name)
        # print(dir)
        if not os.path.exists(dir):
            os.makedirs(dir)

        output_file = os.path.join(dir, str(name))
        # print(output_file)

        with requests.session() as session:
            response = session.get(url)
            if response.status_code == 200:
                if not os.path.exists(output_file):
                    with open(output_file, 'wb') as f:
                        f.write(response.content)
                    print("File downloaded successfully.")
                    return True
                else:
                    print("File already exists.")
                    return True
            else:
                print("Failed to download the file.")
                return False
        
