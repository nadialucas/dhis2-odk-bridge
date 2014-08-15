import requests, json, code

dhis2_url = "http://212.71.248.145:8080/ccei_laos/api/"
auth=('admin', 'district')
headers = {'content-type': 'application/json'}

def get(url):
    return requests.get(dhis2_url+url,auth=auth)

#acquire data elements
dataSets_url = "dataSets"
dataSetsApi = get(dataSets_url)
json1_str = dataSetsApi.text
json1_data = json.loads(json1_str)
json1_data['dataSets']
dataSets = json1_data['dataSets']
idList = []
for i in range(len(dataSets)):
    ID = dataSets[i]['id']
    idList.append(ID)

elementList = []
for i in idList:
    dataElementList = []
    dataSet_url = "dataSets/"+str(i)
    dataSetApi = get(dataSet_url)
    json2_str = dataSetApi.text
    json2_data = json.loads(json2_str)
    periodType = json2_data['periodType']
    name = json2_data['name']
    elementList.append(name)
    dataElements = json2_data['dataElements']
    for i in range(len(dataElements)):
        elementList.append(dataElements[i]['name'])
        dataElement_url = "dataElements/"+str(dataElements[i]['id'])
        dataElementApi = get(dataElement_url)
        json3_str = dataElementApi.text
        json3_data = json.loads(json3_str)
        if 'optionSet' in json3_data.keys():
   			for i in json3_data['optionSet']['options']:
   				elementList.append(i)

d={}
for i in elementList:
	d[i]=u' '

d['Select Province:'] = u' '
d['Select District:'] = u' '
d['Select Facility:'] = u' '
d['Select Equipment:'] = u' '
d['English'] = u' '
d['Lao'] = u' '
# explain the nature of the break to Lee
d['In order to switch languages to Lao, press the button labelled'] = u' '
d['in the top left of the survey form.  Then select Language (the first button) and switch to Lao.'] = u' '
d['In order to switch languages to English, press the button labelled'] = u' '
d['in the top left of the survey form.  Then select Language (the first button) and switch to English.'] = u' '
d['What month is this data entry for?'] = u' '
d['Whaat year is this data entry for?'] = u' '


s = json.dumps(d)
f = open("lao_translations.json", "w")
f.write(s)
f.close()




translations_json_str = open("lao_translations.json").read()
translations_json_data = json.loads(translations_json_str)


