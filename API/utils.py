import requests
import json
import sys

class utils:

    def __init__(self, baseUrl, datasetName):
        self.baseUrl = baseUrl
        self.token = None
        self.datasetName = datasetName

    def sendRequest(self,url, data):  
        json_data = json.dumps(data)

        if self.token == None:
            response = requests.post(url, json_data)
        else:
            headers = {'X-Auth-Token': self.token}              
            response = requests.post(url, json_data, headers = headers)    

        try:
            httpStatusCode = response.status_code 
            if response == None:
                print("No output from service")
                sys.exit()
            output = json.loads(response.text)	
            if output['errorCode'] != None:
                print(output['errorCode'], "- ", output['errorMessage'])
                sys.exit()
            if  httpStatusCode == 404:
                print("404 Not Found")
                sys.exit()
            elif httpStatusCode == 401: 
                print("401 Unauthorized")
                sys.exit()
            elif httpStatusCode == 400:
                print("Error Code", httpStatusCode)
                sys.exit()
        except Exception as e: 
                response.close()
                print(e)
                sys.exit()
        response.close()

        return output['data']

    def generateKey(self,username,password):
        url = self.baseUrl + "login"
        payload = {
            "username": username,
            "password": password
        }

        # Sending a POST request with JSON payload
        self.token = self.sendRequest(url, payload)
        return self.token

    def datasetSearch(self,datasetName=""):
        url = self.baseUrl + "dataset-search"
        payload = {
            "datasetName": datasetName
        }
        return self.sendRequest(url, payload)
    
    def sceneSearch(self,maxResults,startingNumber,spatialFilter,acquisitionFilter):
        url = self.baseUrl + "scene-search"
        payload = {
            "datasetName": self.datasetName,
            "maxResults": maxResults,
            "startingNumber": startingNumber,
            "sceneFilter": {
                "spatialFilter": spatialFilter,
                "acquisitionFilter": acquisitionFilter
            }
        }

        return self.sendRequest(url, payload)

    def downloadOptions(self,sceneIds):
        url = self.baseUrl + "download-options"
        payload = {
            "datasetName": self.datasetName,
            "entityIds": sceneIds
        }

        return self.sendRequest(url, payload)

    def downloadRequest(self,downloads,label):
        url = self.baseUrl + "download-request"
        payload = {
            "downloads": downloads,
            "label": label
        }

        return self.sendRequest(url, payload)
