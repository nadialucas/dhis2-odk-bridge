import json, code, requests

dhis2_url = "http://212.71.248.145:8080/ccei_laos/api/"
auth=('admin', 'district')
headers = {'content-type': 'application/json', 'accept':'application/json'}


def get(url):
    return requests.get(dhis2_url+url,auth=auth)

aggregate_url = "https://cceilaosform.appspot.com/odktables/tables/tables/"

def put(url, payload):
	return requests.put(aggregate_url+str(url), headers = headers, data = payload)

dataSet_url = "dataSets"

dataSetApi = get(dataSet_url)
json1_str = dataSetApi.text
json1_data = json.loads(json1_str)
dataSets = json1_data['dataSets']
idList = []
for i in range(len(dataSets)):
    ID = dataSets[i]['id']
    idList.append(ID)

#Acquiring data elements


tableDict = {}
for i in idList:
	dataElement_url = "dataSets/"+str(i)
	dataElementApi = get(dataElement_url)
	json2_str = dataElementApi.text
	json2_data = json.loads(json2_str)
	dataElements = json2_data['dataElements']
	oldDict = {}
	columnList = []
	for j in dataElements:
		newDict={}
		newDict['elementKey']= j['id']
		newDict['elementName'] = j['id']
		element_url = "dataElements/"+str(j['id'])
		element_info = get(element_url)
		json3_str = element_info.text
		json3_data = json.loads(json3_str)
		name = json3_data['name']
		newDict['tableId'] = json3_data['dataSets'][0]['id']
		dhis2Type = json3_data['type']
		if 'optionSet' in json3_data.keys():
			aggType = 'select_one'
		elif dhis2Type == 'string':
			aggType = 'text'
		elif dhis2Type == 'int':
			aggType = 'integer'
		newDict['elementType'] = aggType
		newDict['listChildElementKeys'] = 'null'
		newDict['idUnitOfRetention'] = 1
		columnList.append(newDict)
	nameDict = {}
	nameDict['tableId'] = i
	nameDict['columns']=columnList
	tableDict[i] = nameDict

for i in tableDict.keys():
	pay = json.dumps(tableDict[i])
	r = put(i, pay)



    
