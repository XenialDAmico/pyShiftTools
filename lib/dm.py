import requests,json

debug = 0

def getPayrollCutoverTime(dmURL, token, companyid, sites):
    headers = {
        'authorization': token,
        'x-company-id': companyid,
        'x-site-ids': sites,
        'Content-Type': 'application/json',
        'Connection': "keep-alive",
        'cache-control': "no-cache"
        }

    strURL = "/business-rule-group/master?$filter=(is_active%20eq%20in(true))&$select=name,description&$top=50&include_site_versions=false&split_site_documents=false"
    fullDM_URL = dmURL + strURL
    try:
        res = requests.request("GET", fullDM_URL, headers=headers)
    except requests.exceptions.HTTPError as errh:
        print ("ERROR - HTTP ERROR:",errh)
        exit()
    except requests.exceptions.Timeout as errt:
        print ("ERROR - TIMEOUT:",errt)  
        exit()
    except requests.exceptions.ConnectionError as errc:
        print ("ERROR - CONNECTION ISSUE:",errc) 
        exit() 
    except requests.exceptions.RequestException as e:
        # catastrophic error. bail.
        print ("ERROR - ANOTHER ISSUE:",e) 
        exit()

    busRules = res.text
    busRulesJSON = json.loads(busRules)

    if debug==1:
        print("Response JSON for Business Rules:" + json.dumps(busRules, indent=4, sort_keys=True))
        print("----------------------------------------------")
    
    for rule in busRulesJSON["items"]:
        if rule["name"] == 'Payroll':
            doc_id = rule["_id"]
            doc_details = getBusRuleDocument(dmURL,token,companyid,sites,doc_id)
            for detail in doc_details["business_rule_items"]:
                if debug:
                    print("Business Rule Item:" + detail)
                if detail["name"] == "PayPeriodStartTimeOfDay":
                    payroll_cutover = detail["value"]
    return payroll_cutover

def getBusRuleDocument(dmURL, token, companyid, sites, doc_id):
    headers = {
        'authorization': token,
        'x-company-id': companyid,
        'x-site-ids': sites,
        'Content-Type': 'application/json',
        'Connection': "keep-alive",
        'cache-control': "no-cache"
        }

    strURL = "/business-rule-group/document/" + doc_id + "?include_mappings=true&include_inactive=false"
    dmURL = dmURL + strURL
    if debug:
        print("Calling DM Api with URL: " + dmURL)

    try:    
        res = requests.request("GET", dmURL, headers=headers)
    except requests.exceptions.HTTPError as errh:
        print ("ERROR - HTTP ERROR:",errh)
        exit()
    except requests.exceptions.Timeout as errt:
        print ("ERROR - TIMEOUT:",errt)  
        exit()
    except requests.exceptions.ConnectionError as errc:
        print ("ERROR - CONNECTION ISSUE:",errc) 
        exit() 
    except requests.exceptions.RequestException as e:
        # catastrophic error. bail.
        print ("ERROR - ANOTHER ISSUE:",e) 
        exit()

    payResObj = res.text
    payResJSON = json.loads(payResObj)
    if debug==1:
        print("Response JSON for Business Rule Document:" + json.dumps(payResJSON, indent=4, sort_keys=True))
        print("----------------------------------------------")
    return payResJSON

def getPayTypes(dmURL, token, companyid, sites):
    headers = {
        'authorization': token,
        'x-company-id': companyid,
        'x-site-ids': sites,
        'Content-Type': 'application/json',
        'Connection': "keep-alive",
        'cache-control': "no-cache"
        }

    strURL = "/pay-type/master"

    dmURL = dmURL + strURL
    res = requests.request("GET", dmURL, headers=headers)

    if res.status_code != 200:
        print(("ERROR GETTING Pay Type DATA: Status Code returned of " + str(res.status_code)))
        exit()
    payResObj = res.text

    payResJSON = json.loads(productResObj)
    if debug==1:
        print("Response JSON for Pay Types:" + json.dumps(payResJSON, indent=4, sort_keys=True))
        print("----------------------------------------------")
    return payResJSON


def getVariantByEntityId(dmURL, token, companyid, sites, entityId, date):
    headers = {
        'authorization': token,
        'x-company-id': companyid,
        'x-site-ids': sites,
        'Content-Type': 'application/json',
        'Connection': "keep-alive",
        'cache-control': "no-cache"
        }

    strURL = "/variant/current?entity_ids=['" + entityId  + "']&effective_date=" + date + "T00:00:00.000Z"

    dmURL = dmURL + strURL
    try:
        res = requests.request("GET", dmURL, headers=headers)
    except requests.exceptions.HTTPError as errh:
        print ("ERROR - HTTP ERROR:",errh)
        exit()
    except requests.exceptions.Timeout as errt:
        print ("ERROR - TIMEOUT:",errt)  
        exit()
    except requests.exceptions.ConnectionError as errc:
        print ("ERROR - CONNECTION ISSUE:",errc) 
        exit() 
    except requests.exceptions.RequestException as e:
        # catastrophic error. bail.
        print ("ERROR - ANOTHER ISSUE:",e) 
        exit()

    variantResObj = res.text
    variantResJSON = json.loads(variantResObj)

    if debug==1:
        print("Response JSON for Variant:" + json.dumps(variantResJSON, indent=4, sort_keys=True))
        print("----------------------------------------------")
    return variantResJSON

def getModifierGroupByEntityId(dmURL, token, companyid, sites, entityId, date):
    headers = {
        'authorization': token,
        'x-company-id': companyid,
        'x-site-ids': sites,
        'Content-Type': 'application/json',
        'Connection': "keep-alive",
        'cache-control': "no-cache"
        }

    strURL = "/modifier-group/current?entity_ids=['" + entityId  + "']&effective_date=" + date + "T00:00:00.000Z"
    dmURL = dmURL + strURL

    try:
        res = requests.request("GET", dmURL, headers=headers)
    except requests.exceptions.HTTPError as errh:
        print ("ERROR - HTTP ERROR:",errh)
        exit()
    except requests.exceptions.Timeout as errt:
        print ("ERROR - TIMEOUT:",errt)  
        exit()
    except requests.exceptions.ConnectionError as errc:
        print ("ERROR - CONNECTION ISSUE:",errc) 
        exit() 
    except requests.exceptions.RequestException as e:
        # catastrophic error. bail.
        print ("ERROR - ANOTHER ISSUE:",e) 
        exit()

    modifierGroupResObj = res.text

    modifierGroupResJSON = json.loads(modifierGroupResObj)
    if debug==1:
        print("Response JSON for Modifier Group:" + json.dumps(modifierGroupResJSON, indent=4, sort_keys=True))
        print("----------------------------------------------")
    return modifierGroupResJSON

def getMasterProducts(dmURL, token, companyid,  date,  include_prices, tag):
    headers = {
        'authorization': token,
        'x-company-id': companyid,
        'Content-Type': 'application/json',
        'Connection': "keep-alive",
        'cache-control': "no-cache"
        }

    strURL = "/product/master?$top=500&$select=product_id,name,entity_id"
    if include_prices:
        strURL = strURL + "&$expand=product-price"
    if tag:
        strURL = strURL + "&$filter=product_tag_entity_ids eq '" + tag + "'"


    dmURL = dmURL + strURL
    if debug:
        print("Calling DM to get Products: " + dmURL)
    
    try:
        res = requests.request("GET", dmURL, headers=headers)
    except requests.exceptions.HTTPError as errh:
        print ("ERROR - HTTP ERROR:",errh)
        exit()
    except requests.exceptions.Timeout as errt:
        print ("ERROR - TIMEOUT:",errt)  
        exit()
    except requests.exceptions.ConnectionError as errc:
        print ("ERROR - CONNECTION ISSUE:",errc) 
        exit() 
    except requests.exceptions.RequestException as e:
        # catastrophic error. bail.
        print ("ERROR - ANOTHER ISSUE:",e) 
        exit()

    prductsResObj = res.text
    prductsResObjJSON = json.loads(prductsResObj)
    
    if debug==1:
        print("Response JSON for Products:" + json.dumps(prductsResObjJSON, indent=4, sort_keys=True))
        print("----------------------------------------------")
    return prductsResObjJSON