import requests, json, code

dateDict = {'Jan':'01', 'Feb':'02', 'Mar':'03', 'Apr':'04', 'May':'05', 'Jun':'06',
            'Jul':'07', 'Aug':'08', 'Sep':'09', 'Oct':'10', 'Nov':'11', 'Dec':'12'}

###### GET REQUEST FROM AGGREGATE ######

headers = {'accept': 'application/json'}
aggregate_url = "https://cceilaosform.appspot.com/odktables/tables/tables"

###### GET REQUEST FROM DHIS2 #######
dhis2_url = "http://212.71.248.145:8080/ccei_laos/api/"
auth=('admin', 'district')
headers = {'content-type': 'application/json'}
def get(url):
    return requests.get(dhis2_url+url,auth=auth)
r = get("dataSets")
json5_str = r.text
json5_data = json.loads(json5_str)
periodTypeDict = {}
for i in json5_data['dataSets']:
    p = get("dataSets/"+str(i['id']))
    json6_str = p.text
    json6_data = json.loads(json6_str)
    periodTypeDict[str(i['id'])] = json6_data['periodType']
    
y = get("dataElements/XcsRylFgV6m")
print y.text                   


### issues a GET request to retrieve tableId and schemaETag of all forms in aggregate ###
y = requests.get(aggregate_url, headers=headers)
json1_str = y.text
json1_data = json.loads(json1_str)
entries = json1_data['entries']
IdETagList = []
for i in range(len(entries)):
    tableId = entries[i]['tableId']
    schemaETag = entries[i]['schemaETag']
    payload = {"dataSet": str(tableId),
               "dataValues":[]}
    ### issues GET request for data in each individual form ###
    p = requests.get(aggregate_url+"/"+tableId+"/"+schemaETag+"/rows", headers=headers)
    json2_str = p.text
    json2_data = json.loads(json2_str)
    entries2 = json2_data['entries']
    json2_entries = entries2[0]
    values = json2_entries['values']
    for k in values.keys():
        if k=="date":
            if periodTypeDict[tableId] == 'Monthly':
                mon = values[k][0:3]
                monNum = dateDict[mon]
                year = values[k][7:]
                payload["period"]=year+num
            else:
                year = values[k][7:]
                payload["period"]=year
        elif k=="facility_id":
            payload["orgUnit"]=str(values[k])
        else:
            payload["dataValues"].append({"dataElement":str(k), "value":str(values[k])})
    ##### POST REQUEST TO DHIS2 #####
    dhis2_url = "http://212.71.248.145:8080/ccei_laos/api/dataValueSets"
    auth=('admin', 'district')
    headers2 = {'content-type': 'application/json'}
    payload=json.dumps(payload)
    r = requests.post(dhis2_url, auth=auth, headers=headers2, data=payload)

if __name__ == '__main__':
    code.interact(local=locals())

'''
##### POST REQUEST TO DHIS2 #####

dhis2_url = "http://212.71.248.145:8080/ccei_laos/api/dataValueSets"
auth=('admin', 'district')
headers = {'content-type': 'application/json'}

## POST functionality ##

def post(payload):
    headers = {'content-type': 'application/json'}
    return requests.post(dhis2_url, auth=auth, headers=headers, data=payload)

def post_dataset(dataSet,period,orgUnit,payload):
    return post("dataValueSets?dataSet=%s&period=%s&orgUnit=%s"%(dataSet,period,orgUnit),payload)

## GET functionality still under construction here ##
    
def get(url):
    return requests.get(dhis2_url+url,auth=auth)



## constructing the payload with the data elements retrieved from Aggregate ##

if __name__ == '__main__':
    payload = {"dataSet": "FIeVtefCGzw",  "period": str(period),  "orgUnit": str(orgUnit),
               "dataValues": [{ "dataElement": "drdP9msdelZ", "value": str(population) },{ "dataElement": "SorlQvheiqX", "value": str(coverage)},
                              { "dataElement": "HOaK9H7m7s9", "value": str(storageType)},{ "dataElement": "zWa0eHtVeM4", "value": str(deliveryType)},
                              {"dataElement": "BWS4ldV2D6c", "value": str(electricitySource)},       {"dataElement": "TvSsPzAM5ht", "value": str(gridAvailability)},
                              {"dataElement": "XcsRylFgV6m", "value": str(gasAvailability)}, {"dataElement": "fmX8c6SpdiZ", "value": str(keroseneAvailability)},
                              {"dataElement": "XXRQpn99jEV", "value": str(climateSuitable)}, {"dataElement": "k45dPuwe3z6", "value": str(siteSuitable)},
                              {"dataElement": "d2R87vcTgw3", "value": str(supplyInterval)}, {"dataElement": "OBSS7mj0jYO", "value": str(reserveStock)},
                              {"dataElement": "woy5UWG6J2A", "value": str(distanceSupply)}, {"dataElement": "UkKzPZXovTN", "value": str(mainPoint)},
                              {"dataElement": "oGmnCOjGBYi", "value": str(secondaryPoint)}, {"dataElement": "nxJwVcwmC5C", "vale": str(modeSupply)}]}

    payload=json.dumps(payload)
    m = post(payload)
    #drop into python with all local variables
    code.interact(local=locals())

'''

