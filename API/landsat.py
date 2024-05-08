from utils import utils 
from datetime import datetime, timedelta
import requests
import os
from landsatxplore.api import API
import shutil

download_directory = ("downloads/{image_name}")

def Landsat(baseUrl,datasetName,lat,lon,sdate,edate):

    returnMessage = {
        'success':False,
        'error':(None,"")
    }

    directory_to_delete = 'downloads'
    try:
        shutil.rmtree(directory_to_delete)
        print("Directory", directory_to_delete, "successfully deleted.")
    except FileNotFoundError:
        pass
    except Exception as e:
        print("An error occurred:", e)

    api = utils(baseUrl,datasetName)
    api.generateKey("musutfa","Playstore123$")

    # Initialize a new API instance and get an access key
    xplorer = API("MurtazaAliKhokhar", "fLZEwWdaE|e78_S")

    scenes = []

    num_scenes = 2

    if edate:
        # print("yes edate")
        num_scenes = 1
        scene = findScenes(xplorer,lat,lon,edate,num_scenes)
        scenes.extend(scene)

    scene = findScenes(xplorer,lat,lon,sdate,num_scenes)
    scenes.extend(scene)

    scene1_date = scenes[0]['acquisition_date'].strftime('%Y-%m-%d')
    scene2_date = scenes[1]['acquisition_date'].strftime('%Y-%m-%d')
    dprint("First Scene Acquired for",scene1_date)
    dprint("Second Scene Acquired for",scene2_date)

    sceneIds = []
    band_names_tif = []
    band_names = ['3','5']
    # band_names = ['7']
    for bn in band_names:
        string = "_SR_B"+bn+"_TIF"
        band_names_tif.append(string)
    # band_names_tif = ["_SR_B3_TIF","_SR_B5_TIF","_SR_B6_TIF","_SR_B7_TIF"]
    #band_names_tif = ["_QA_PIXEL_TIF","_QA_RADSAT_TIF","_SR_B1_TIF","_SR_B2_TIF","_SR_B3_TIF","_SR_B4_TIF","_SR_B5_TIF","_SR_B6_TIF","_SR_B7_TIF"]
    for scene in scenes:
        # print(scene)
        for band in band_names_tif:
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

    label = datetime.now().strftime("%Y%m%d%H%M%S")
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

def findScenes(xplorer,lat,lon,date,num_scenes):

    # print("trying to find scene for",date)
    # print("scenes num",num_scenes)

    scenes = []

    sdate=date

    while len(scenes)<num_scenes:
        scenes = xplorer.search(
            dataset='landsat_ot_c2_l2',
            latitude=lat,
            longitude=lon,
            start_date=sdate,
            end_date=date,
            max_cloud_cover=25
        )
        sdate = datetime.strptime(sdate, '%Y-%m-%d')
        sdate = sdate - timedelta(days=1)
        sdate = sdate.strftime('%Y-%m-%d')
        # print("changed to",sdate)

    # print("lets see our luck")

    # print(f"{len(scenes)} scenes found.")
    return scenes

def dprint(*args):
    print(*args)
    print("--------------------------")

def downloadFile(url, name):
    
    n = name.split('_')
    short_name = '_'.join(n[1:8])

    dir = download_directory.format(image_name=short_name)

    if not os.path.exists(dir):
        os.makedirs(dir)

    tifless_name = name[:-4]
    band = tifless_name[-2:]
    name = band+'.TIF'

    output_file = os.path.join(dir, str(name))
    # print(output_file)

    print("Downloading",name)
    print("testing")
    with requests.session() as session:
        print("requesting session")
        print(url)
        response = session.get(url)
        print("got response")
        if response.status_code == 200:
            print("downloading from here")
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
        
