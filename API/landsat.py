import utils as ut
import datetime

def Landsat(baseUrl,datasetName):

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
                     
    api = ut.utils(baseUrl,datasetName)
    token = api.generateKey("musutfa","Playstore123$")
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

    dprint("Scenes found: ", scenes['recordsReturned'])
    sceneIds = []
    for scene in scenes['results']:
        sceneIds.append(scene['entityId'])

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
    requestedDownloads = len(downloads)
    label = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    requestResults = api.downloadRequest(downloads, label)
    if not requestResults['availableDownloads']:
        returnMessage['message'] = "No download options found"
        return returnMessage

    # print("Requested downloads: ", requestResults)

    downloadLinks = dict()
    for download in requestResults['availableDownloads']:
        # print(download)
        name = download['url'].split('/')[-1].split('?')[0]
        if name in downloadLinks:
            downloadLinks[name].append(download['url'])
        else:
            downloadLinks[name] = [download['url']]
        
    for i in downloadLinks:
        dprint("Download options for ",i)
        for idx,j in enumerate(downloadLinks[i]):
            dprint(str(idx+1)+")",j)

    returnMessage['succes'] = True
    return returnMessage

def dprint(*args):
    print(*args)
    print("--------------------------")