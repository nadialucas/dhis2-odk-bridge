import requests, json, code, xlsxwriter
#uncomment to enable Lao version of form
#import lao_translations.json


#comment out the following when ccei equipment GET requests are fixed
cceiFormIds = []
#uncomment out the following when ccei equipment GET requests are fixed
#cceiFormIds = ['G3qzd30RrrG']

dhis2_url = "http://212.71.248.145:8080/ccei_laos/api/"
auth=('admin', 'district')
headers = {'content-type': 'application/json'}

def get(url):
    return requests.get(dhis2_url+url,auth=auth)

#uncomment to enable Lao version of form
#translations_json_str = open("lao_translations.json").read()
#translations_json_data = json.loads(translations_json_str)


#Acquiring data sets


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

elementLists = []
administrationLists = []
#create an elementList and an administrationList for each dataSet
for i in idList:
    dataElementList = []
    administrationElements = [i]
    dataElement_url = "dataSets/"+str(i)
    dataElementApi = get(dataElement_url)
    json2_str = dataElementApi.text
    json2_data = json.loads(json2_str)
    periodType = json2_data['periodType']
    name = json2_data['name']
    administrationElements.append(name)
    administrationElements.append(periodType)
    administrationLists.append(administrationElements)
    dataElements = json2_data['dataElements']
    for i in range(len(dataElements)):
        dataElementList.append(dataElements[i]['id'])
    elementLists.append(dataElementList)

# Data elements acquired
# Acquire OrgUnit Data


        

        


# Get details about data elements
# Create xlsx form



def xlsxCreator(elementList, adminList):
    workbook = xlsxwriter.workbook.Workbook(str(adminList[0])+".xlsx")

    #worksheet titles
    worksheet1 = workbook.add_worksheet('survey')
    worksheet2 = workbook.add_worksheet('settings')
    worksheet3 = workbook.add_worksheet('choices')

    #survey titles
    worksheet1.write(0,0,'type')
    worksheet1.write(0,1,'values_list')
    worksheet1.write(0,2,'name')
    worksheet1.write(0,3,'display.text')
    worksheet1.write(0,4,'display.hint')
    worksheet1.write(0,5,'choice_filter')
    worksheet1.write(0,6,'display.text.lao')
    worksheet1.write(0,7,'display.hint.lao')
    worksheet1.write(0,8,'scrollerAttributes.dateOrder')
    worksheet1.write(0,9,'scrollerAttributes.preset')
    worksheet1.write(0,10,'scrollerAttributes.theme')
    worksheet1.write(0,11,'scrollerAttributes.display')
    worksheet1.write(0,12,'model.isSessionVariable')

    #settings titles
    worksheet2.write(0,0,'setting_name')
    worksheet2.write(0,1,'value')
    worksheet2.write(0,2,'display.title')
    worksheet2.write(0,3,'display.title.lao')
    worksheet2.write(0,4,'display.text')
    worksheet2.write(0,5,'display.text.lao')
    worksheet2.write(1,0,'form_id')
    worksheet2.write(2,0,'form_version')
    worksheet2.write(3,0,'survey')
    worksheet2.write(4,0,'default')
    worksheet2.write(5,0,'lao')
    worksheet2.write(6,0,'hideNavigationButtonText')

    #choices titles
    worksheet3.write(0,0,'choice_list_name')
    worksheet3.write(0,1,'data_value')
    worksheet3.write(0,2,'display.text')
    worksheet3.write(0,3,'province')
    worksheet3.write(0,4,'district')
    if adminList[0] in cceiFormIds:
        worksheet3.write(0,5,'facilities')
    #append here to add level 5 functionality

    #settings content
    worksheet2.write(1,1, str(adminList[0]))
    worksheet2.write(2,1,'20140812')
    worksheet2.write(3,2, str(adminList[1]))
    # uncomment to enable Lao version of form
    #worksheet2.write(4,4,translations_json_data['English'])
    #worksheet2.write(5,4,translations_json_data['Lao'])
    #worksheet2.write(4,5,'English')
    #worksheet2.write(5,5,'Lao')
    #worksheet2.write(6,1,'TRUE')

    #survey content (and creating optionDict)
    worksheet1.write(1,0,'note')
    #uncomment to enable Lao version of form
    #worksheet1.write(1,3,'In order to switch languages to Lao, press the button labelled'+str(adminList[1])+'in the top left of the survey form.  Then select Language (the first button) and switch to Lao.'+translations_json_data['In order to switch languages to Lao, press the button labelled']+str(adminList[1])+translations_json_data['in the top left of the survey form.  Then select Language (the first button) and switch to Lao.'])
    #worksheet1.write(1,6,'In order to switch languages to English, press the button labelled'+str(adminList[1])+'in the top left of the survey form.  Then select Language (the first button) and switch to English.'+translations_json_data['In order to switch languages to English, press the button labelled']+str(adminList[1])+translations_json_data['in the top left of the survey form.  Then select Language (the first button) and switch to English.']
    worksheet1.write(2,0,'date')
    worksheet1.write(2,2,'date')
    #write in the correct time widget to the xlsx form
    if adminList[2]=='Monthly':
        worksheet1.write(2,3,'What month is this data entry for?')
        #uncomment to enable Lao version of form
        #worksheet1.write(2,6,translations_json_data['What month is this data entry for?'])
        worksheet1.write(2,8,'mmyy')
        worksheet1.write(2,9,'date')
        worksheet1.write(2,10,'jqm')
        worksheet1.write(2,11,'modal')
    elif adminList[2]=='Yearly':
        worksheet1.write(2,3,'What year is this data entry for?')
        #uncomment to enable Lao version of form
        #worksheet1.write(2,6,translations_json_data['What year is this data entry for?'])
        worksheet1.write(2,8,'yy')
        worksheet1.write(2,9,'date')
        worksheet1.write(2,10,'jqm')
        worksheet1.write(2,1,'modal')
    worksheet1.write(3,0,'select_one')
    worksheet1.write(3,1,'provinces')
    worksheet1.write(3,2,'province_id')
    worksheet1.write(3,12,'TRUE')
    worksheet1.write(3,3,'Select Province:')
    # uncomment to enable Lao version of form
    #worksheet1.write(3,6,translations_json_data['Select Province:'])
    worksheet1.write(4,0,'select_one')
    worksheet1.write(4,1,'districts')
    worksheet1.write(4,2,'district_id')
    worksheet1.write(4,12,'TRUE')
    worksheet1.write(4,3,'Select District:')
    # uncomment to enable Lao version of form
    #worksheet1.write(4,6,translations_json_data['Select District:'])
    worksheet1.write(4,4,"choice_item.province===data('province')")
    worksheet1.write(5,0,'select_one')
    worksheet1.write(5,1,'facilities')
    worksheet1.write(5,2,'facility_id')
    worksheet1.write(5,3,'Select Facility:')
        # uncomment to enable Lao version of form
    #worksheet1.write(5,6,translations_json_data['Select Facility:'])
    worksheet1.write(5,4,"choice_item.district===data('district')")
    if adminList[0] in cceiFormIds:
        worksheet1.write(6,0,'select_one')
        worksheet1.write(6,1,'equipments')
        worksheet1.write(6,2,'equipment_id')
        worksheet1.write(6,3,'Select Equipment:')
        # uncomment to enable Lao version of form
        #worksheet1.write(6,6,translations_json_data['Select Equipment:'])
        worksheet1.write(6,4,"choice_item.facility===data('facility')")

    #create options for those forms that have select_one questions
    optionDict = {}
    if adminList[0] in cceiFormIds:
        for i in range(len(elementList)):
            elementApi = get('dataElements/'+str(elementList[i]))
            json3_str = elementApi.text
            json3_data = json.loads(json3_str)
            if 'optionSet' in json3_data.keys():
                worksheet1.write(i+7,0,'select_one')
                worksheet1.write(i+7,1,'conditions'+str(i))
                optionSet = json3_data['optionSet']
                options = optionSet['options']
                optionDict['conditions'+str(i)] = options
            else:    
                elementType = json3_data['type']
                if elementType == 'int':
                    worksheet1.write(i+7,0,'integer')
                elif elementType == 'string':
                    worksheet1.write(i+7,0,'text')
            elementId = elementList[i]
            worksheet1.write(i+7,2,elementId)
            elementName = json3_data['name']
            worksheet1.write(i+7,3,elementName)
            #uncomment to enable Lao version of form
            #worksheet1.write(i+7,6,translations_json_data[elementName])


    else:
        for i in range(len(elementList)):
            elementApi = get('dataElements/'+str(elementList[i]))
            json3_str = elementApi.text
            json3_data = json.loads(json3_str)
            if 'optionSet' in json3_data.keys():
                worksheet1.write(i+6,0,'select_one')
                worksheet1.write(i+6,1,'conditions'+str(i))
                optionSet = json3_data['optionSet']
                options = optionSet['options']
                optionDict['conditions'+str(i)] = options
            else:    
                elementType = json3_data['type']
                if elementType == 'int':
                    worksheet1.write(i+6,0,'integer')
                elif elementType == 'string':
                    worksheet1.write(i+6,0,'text')
            elementId = elementList[i]
            worksheet1.write(i+6,2,elementId)
            elementName = json3_data['name']
            worksheet1.write(i+6,3,elementName)
            #uncomment to enable Lao version of form
            #worksheet1.write(i+6,6,translations_json_data[elementName])

    #choices content
    count = 1
    for k in optionDict.keys():
        for j in range(len(optionDict[k])):
            worksheet3.write(count+j,0,k)
            worksheet3.write(count+j,1,optionDict[k][j])
            worksheet3.write(count+j,2,optionDict[k][j])
            #uncomment to enable Lao version of form
            #worksheet3.write(count+j,5,translations_json_data[optionDict[k][j]])
        count+=len(optionDict[k])

    #set up orgUnitList
    if adminList[0] in cceiFormIds:
        orgUnitList=[]
        idVariable = adminList[0]
        dataSets_url = "dataSets/"+str(idVariable)
        dataSets_Api = get(dataSets_url)
        json4_str = dataSets_Api.text
        json4_data = json.loads(json4_str)
        orgUnits = json4_data['organisationUnits']
        orgUnitParentList = []
        for k in range(len(orgUnits)):
            orgUnitList.append([orgUnits[k]['id'],orgUnits[k]['name']])
        for j in orgUnitList:
            orgUnit_url = "organisationUnits/"+str(j[0])
            orgUnit1 = get(orgUnit_url)
            json5_str = orgUnit1.text
            json5_data = json.loads(json5_str)
            orgUnit1Parent = json5_data['parent']
            #this checks to see if the parent is Lao PDR or not
            if orgUnit1Parent['id']!='IWp9dQGM0bS':
                if orgUnit1Parent['id'] not in orgUnitParentList:
                    orgUnitParentList.append(orgUnit1Parent['id'])
                    j.append(orgUnit1Parent['id'])
                    j.append(orgUnit1Parent['name'])
                #if the parent has already been fetched then the parent is simply named "repeat" but the id is still the parent id
                else:
                    j.append(orgUnit2Parent['id'])
                    j.append('repeat')
                orgUnit2_url = 'organisationUnits/'+str(j[2])
                orgUnit2 = get(orgUnit2_url)
                json6_str = orgUnit2.text
                json6_data = json.loads(json6_str)
                orgUnit2Parent['id'] = json6_data['parent']
                if orgUnit2Parent['id']!='IWp9dQGM0bS':
                    if orgUnit2Parent not in orgUnitParentList:
                        orgUnitParentList.append(orgUnit2Parent['id'])
                        j.append(orgUnit2Parent['id'])
                        j.append(orgUnit2Parent['name'])
                    else:
                        j.append(orgUnit2Parent['id'])
                        j.append('repeat')
                    j.append(orgUnit2Parent['id'])
                    j.append(orgUnit2Parent['name'])
                    orgUnit3_url = 'organisationUnits/'+str(j[4])
                    orgUnit3 = get(orgUnit3_url)
                    json7_str = orgUnit3.text
                    json7_data = json.loads(json7_str)
                    orgUnit3Parent = json7_data['parent']
                    if orgUnit3Parent['id']!='IWp9dQGM0bS':
                        if orgUnit3Parent['id'] not in orgUnitParentList:
                            j.append(orgUnit3Parent['id'])
                            j.append(orgUnit3Parent['name'])
                        else:
                            j.append(orgUnit3Parent['id'])
                            j.append('repeat')
        equipList = []
        equip_url = "equipments"
        equipApi = get(equip_url)
        json8_str = equipApi.text
        json8_data = json.loads(json8_str)
        for h in json8_data['equipments']:
            equipList.append((h['id'],h['name']))
        #has not been tested because of failed GET REQUEST!!!
        for x in equipList:
            equipnew_url = "equipments"+str(x[0])
            equipnewApi = eget(equipnew_url)
            json9_str = equipnewApi.text
            json9_data = json.loads(json9_str)
            x.append(json9_data['organisationUnit']['parent']['id'])
        for y in orgUnitList:
            if len(x)==2:
                worksheet3.write(count,0,'provinces')
                worksheet3.write(count,1,x[0])
                worksheet3.write(count,2,x[1])
                worksheet3.write(count+1,0,'districts')
                worksheet3.write(count+1,1,x[0])
                worksheet3.write(count+1,2,x[1])
                worksheet3.write(count+1,3,x[0])
                worksheet3.write(count+2,0,'facilities')
                worksheet3.write(count+2,1,x[0])
                worksheet3.write(count+2,2,x[1])
                worksheet3.write(count+2,3,x[0])
                worksheet3.write(count+2,4,x[0])
                count+=3
            if len(x)==4:
                if x[3]=='repeat':
                    worksheet3.write(count,0,'districts')
                    worksheet3.write(count,1,x[0])
                    worksheet3.write(count,2,x[1])
                    worksheet3.write(count,3,x[2])
                    worksheet3.write(count+1,0,'facilities')
                    worksheet3.write(count+1,1,x[0])
                    worksheet3.write(count+1,2,x[1])
                    worksheet3.write(count+1,3,x[2])
                    worksheet3.write(count+1,4,x[1])
                    count+=2
                else:
                    worksheet3.write(count,0,'provinces')
                    worksheet3.write(count,1,x[2])
                    worksheet3.write(count,2,x[3])
                    worksheet3.write(count+1,0,'districts')
                    worksheet3.write(count+1,1,x[0])
                    worksheet3.write(count+1,2,x[1])
                    worksheet3.write(count+1,3,x[2])
                    worksheet3.write(count+2,0,'facilities')
                    worksheet3.write(count+2,1,x[0])
                    worksheet3.write(count+2,2,x[1])
                    worksheet3.write(count+2,3,x[2])
                    worksheet3.write(count+2,4,x[1])
                    count+=3
            if len(x)==6:
                if x[3]=='repeat':
                    worksheet3.write(count,0,'facilities')
                    worksheet3.write(count,1,x[0])
                    worksheet3.write(count,2,x[1])
                    worksheet3.write(count,3,x[2])
                    worksheet3.write(count,4,x[4])
                    count+=1
                elif x[5]=='repeat':
                    worksheet3.write(count,0,'districts')
                    worksheet3.write(count,1,x[2])
                    worksheet3.write(count,2,x[3])
                    worksheet3.write(count,3,x[4])
                    worksheet3.write(count+1,0,'facilities')
                    worksheet3.write(count+1,1,x[0])
                    worksheet3.write(count+1,2,x[1])
                    worksheet3.write(count+1,3,x[2])
                    worksheet3.write(count+1,4,x[4])
                    count+=2
                else:
                    worksheet3.write(count,0,'provinces')
                    worksheet3.write(count,1,x[4])
                    worksheet3.write(count,2,x[5])
                    worksheet3.write(count+1,0,'districts')
                    worksheet3.write(count+1,1,x[2])
                    worksheet3.write(count+1,2,x[3])
                    worksheet3.write(count+1,3,x[4])
                    worksheet3.write(count+2,0,'facilities')
                    worksheet3.write(count+2,1,x[0])
                    worksheet3.write(count+2,2,x[1])
                    worksheet3.write(count+2,3,x[2])
                    worksheet3.write(count+2,4,x[4])
                    count+=3
        for t in equipList:
            worksheet3.write(count,0,'equipments')
            worksheet3.write(count,1,t[0])
            worksheet3.write(count,2,t[1])
            worksheet3.write(count,5,t[2])

    #basically the same as above but with a provision for the extra level of equipment list
    else:
        orgUnitList=[]
        idVariable = adminList[0]
        dataSets_url = "dataSets/"+str(idVariable)
        dataSets_Api = get(dataSets_url)
        json4_str = dataSets_Api.text
        json4_data = json.loads(json4_str)
        orgUnits = json4_data['organisationUnits']
        orgUnitParentList = []
        for k in range(len(orgUnits)):
            orgUnitList.append([orgUnits[k]['id'],orgUnits[k]['name']])
        for j in orgUnitList:
            orgUnit_url = "organisationUnits/"+str(j[0])
            orgUnit1 = get(orgUnit_url)
            json5_str = orgUnit1.text
            json5_data = json.loads(json5_str)
            orgUnit1Parent = json5_data['parent']
            if orgUnit1Parent['id']!='IWp9dQGM0bS':
                if orgUnit1Parent['id'] not in orgUnitParentList:
                    orgUnitParentList.append(orgUnit1Parent['id'])
                    j.append(orgUnit1Parent['id'])
                    j.append(orgUnit1Parent['name'])
                else:
                    j.append(orgUnit1Parent['id'])
                    j.append('repeat')
                orgUnit2_url = 'organisationUnits/'+str(j[2])
                orgUnit2 = get(orgUnit2_url)
                json6_str = orgUnit2.text
                json6_data = json.loads(json6_str)
                orgUnit2Parent = json6_data['parent']
                if orgUnit2Parent['id']!='IWp9dQGM0bS':
                    if orgUnit2Parent not in orgUnitParentList:
                        orgUnitParentList.append(orgUnit2Parent['id'])
                        j.append(orgUnit2Parent['id'])
                        j.append(orgUnit2Parent['name'])
                    else:
                        j.append(orgUnit2Parent['id'])
                        j.append('repeat')
                    j.append(orgUnit2Parent['id'])
                    j.append(orgUnit2Parent['name'])
                    orgUnit3_url = 'organisationUnits/'+str(j[4])
                    orgUnit3 = get(orgUnit3_url)
                    json7_str = orgUnit3.text
                    json7_data = json.loads(json7_str)
                    orgUnit3Parent = json7_data['parent']
                    if orgUnit3Parent['id']!='IWp9dQGM0bS':
                        if orgUnit3Parent['id'] not in orgUnitParentList:
                            j.append(orgUnit3Parent['id'])
                            j.append(orgUnit3Parent['name'])
                        else:
                            j.append(orgUnit2Parent['id'])
                            j.append('repeat')
        for y in orgUnitList:
            if len(x)==2:
                worksheet3.write(count,0,'provinces')
                worksheet3.write(count,1,x[0])
                worksheet3.write(count,2,x[1])
                worksheet3.write(count+1,0,'districts')
                worksheet3.write(count+1,1,x[0])
                worksheet3.write(count+1,2,x[1])
                worksheet3.write(count+1,3,x[0])
                worksheet3.write(count+2,0,'facilities')
                worksheet3.write(count+2,1,x[0])
                worksheet3.write(count+2,2,x[1])
                worksheet3.write(count+2,3,x[0])
                worksheet3.write(count+2,4,x[0])
                count+=3
            if len(x)==4:
                if x[3]=='repeat':
                    worksheet3.write(count,0,'districts')
                    worksheet3.write(count,1,x[0])
                    worksheet3.write(count,2,x[1])
                    worksheet3.write(count,3,x[2])
                    worksheet3.write(count+1,0,'facilities')
                    worksheet3.write(count+1,1,x[0])
                    worksheet3.write(count+1,2,x[1])
                    worksheet3.write(count+1,3,x[2])
                    worksheet3.write(count+1,4,x[1])
                    count+=2
                else:
                    worksheet3.write(count,0,'provinces')
                    worksheet3.write(count,1,x[2])
                    worksheet3.write(count,2,x[3])
                    worksheet3.write(count+1,0,'districts')
                    worksheet3.write(count+1,1,x[0])
                    worksheet3.write(count+1,2,x[1])
                    worksheet3.write(count+1,3,x[2])
                    worksheet3.write(count+2,0,'facilities')
                    worksheet3.write(count+2,1,x[0])
                    worksheet3.write(count+2,2,x[1])
                    worksheet3.write(count+2,3,x[2])
                    worksheet3.write(count+2,4,x[1])
                    count+=3
            if len(x)==6:
                if x[3]=='repeat':
                    worksheet3.write(count,0,'facilities')
                    worksheet3.write(count,1,x[0])
                    worksheet3.write(count,2,x[1])
                    worksheet3.write(count,3,x[2])
                    worksheet3.write(count,4,x[4])
                    count+=1
                elif x[5]=='repeat':
                    worksheet3.write(count,0,'districts')
                    worksheet3.write(count,1,x[2])
                    worksheet3.write(count,2,x[3])
                    worksheet3.write(count,3,x[4])
                    worksheet3.write(count+1,0,'facilities')
                    worksheet3.write(count+1,1,x[0])
                    worksheet3.write(count+1,2,x[1])
                    worksheet3.write(count+1,3,x[2])
                    worksheet3.write(count+1,4,x[4])
                    count+=2
                else:
                    worksheet3.write(count,0,'provinces')
                    worksheet3.write(count,1,x[4])
                    worksheet3.write(count,2,x[5])
                    worksheet3.write(count+1,0,'districts')
                    worksheet3.write(count+1,1,x[2])
                    worksheet3.write(count+1,2,x[3])
                    worksheet3.write(count+1,3,x[4])
                    worksheet3.write(count+2,0,'facilities')
                    worksheet3.write(count+2,1,x[0])
                    worksheet3.write(count+2,2,x[1])
                    worksheet3.write(count+2,3,x[2])
                    worksheet3.write(count+2,4,x[4])
                    count+=3







#this calls the function xlsxcreator for all datasets in DHIS2 Laos instance
for m in range(len(elementLists)):
    elList = elementLists[m]
    adList = administrationLists[m]
    xlsxCreator(elList,adList)
            
        
    
    
        
        
    
    

    
print 'Done'  
