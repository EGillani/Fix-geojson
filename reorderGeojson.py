import json
import os
import requests
from collections import OrderedDict

def get_response():
    url = '<YOUR URL>'
    #PROXIES
    
    response = requests.get(url)
    if response.status_code != 200:
        print(response.status_code, response.text)
        raise Exception(response.status_code, response.text)
    
    return response.text

#obtained from https://stackoverflow.com/questions/12031482/custom-sorting-python-dictionary
def customsort(dict1 , key_order):
    items = [dict1[k] if k in dict1.keys() else 0 for k in key_order] 
    sorted_dict = OrderedDict()
    for i in range(len(key_order)):
        sorted_dict[key_order[i]] = items[i]
    return sorted_dict

#This is primarly set up to read in the json returned from the API and fix it so its in the correct geojson format so it can be viewed in openstreetmap, QGIS, etc. 
def main():
    #if importing from a file desired file 
    '''
    geojsonFile = 'theFile.json'
    #read in the file 
    with open(geojsonFile, 'r') as thefile:
        data = thefile.read()
        #the feature must be set to upper case, otherwise QGIS will not read it in correctly
        fixed = data.replace('feature', 'Feature')
        temp = json.loads(fixed)   '''

    #get the json response as text first, since we have to fix it first 
    data = get_response()
    #the feature must be set to upper case, otherwise QGIS or whatever map service your using will probably not read it in correctly
    fixed = data.replace('feature', 'Feature')
    #load into dictionary for further manipulation
    temp = json.loads(fixed)  
    
    #the desired keyorder
    keyorder  = ['geometry', 'type' ,'properties']
    
    #go into nested json and use the customsort function to change the order
    for i in range(len(temp['Features'])):
        temp['Features'][i] = customsort(temp['Features'][i],keyorder)    

    #add projection in the new slide 
    x = {"properties":{"name":"ESPG:4326"}}
       
    #set up the new dictionary with projection and add the type of features stored 
    newDictionary = {}
    newDictionary['Features'] = temp['Features']
    newDictionary['crs'] = x 
    newDictionary['type'] = temp['type']
    
    #output to a json
    with open('output.json', 'w') as json_file:
        json.dump(newDictionary, json_file, sort_keys = False, indent = 4)


if __name__ == '__main__':
    main()

