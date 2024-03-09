import utils as ut
import datetime
import requests
import os
from landsatxplore.api import API

download_directory = ("downloads/{image_name}")

def Landsat(baseUrl,datasetName,lat,lon,sdate,edate):

    returnMessage = {
        'success':False,
        'error':(None,"")
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
        start_date=sdate,
        end_date=edate,
        max_cloud_cover=10
    )

    print(f"{len(scenes)} scenes found.")

    latest_date = datetime.datetime.min
    latest_scene = None
    for scene in scenes:
        if scene['date_product_generated'] > latest_date:
            latest_date = scene['date_product_generated']
            latest_scene = [scene]

    dprint("date chosen",latest_date)

    sceneIds = []
    band_names = ["_SR_B3_TIF","_SR_B5_TIF","_SR_B6_TIF","_SR_B7_TIF"]
    #band_names = ["_QA_PIXEL_TIF","_QA_RADSAT_TIF","_SR_B1_TIF","_SR_B2_TIF","_SR_B3_TIF","_SR_B4_TIF","_SR_B5_TIF","_SR_B6_TIF","_SR_B7_TIF"]
    for scene in latest_scene:
        # print(scene)
        for band in band_names:
            scene_name = "L2SR_"+scene['display_id']+band
            # sceneIds.append(scene['display_id'])
            sceneIds.append(scene_name)

    downloadOptions = api.downloadOptions(sceneIds)

    if not downloadOptions:
        returnMessage['error'] = (0,"No download options found")
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
        returnMessage['error'] = (1,"No products available to download right now")
        return returnMessage

    dprint("Products available to download: ", len(downloads))

    label = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    requestResults = api.downloadRequest(downloads, label)
    if not requestResults['availableDownloads']:
        returnMessage['error'] = (2,"No download options found")
        return returnMessage

    # print(len(sceneIds))
    # print(len(int(requestResults['availableDownloads'])/2))

    if len(sceneIds) == int(len(requestResults['availableDownloads'])/2):
        dprint("All downloads available")
    else:
        returnMessage['error'] = (3,"Complete download options not found")
        return returnMessage

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

    returnMessage['success'] = True
    return returnMessage

def dprint(*args):
    print(*args)
    print("--------------------------")

def downloadFile(url, name):
    
    n = name.split('_')
    short_name = '_'.join(n[1:8])

    dir = download_directory.format(image_name=short_name)

    if not os.path.exists(dir):
        os.makedirs(dir)

    name = name[:-4]+'.TIF'

    output_file = os.path.join(dir, str(name))
    # print(output_file)

    print("Downloading",name)

    with requests.session() as session:
        response = session.get(url)
        if response.status_code == 200:
            if not os.path.exists(output_file):
                with open(output_file, 'wb') as f:
                    f.write(response.content)
                dprint("File downloaded successfully.")
                return True
            else:
                dprint("File already exists.")
                return True
        else:
            dprint("Failed to download the file.")
            return False
        
