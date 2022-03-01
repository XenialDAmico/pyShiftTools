
import requests, json

debug = 1

def putShift(xnu_conn, token, companyid,siteid, data):
    
    xnu_headers = {
        'content-type': "application/json",
        'cache-control': "no-cache",
        'authorization': token,
        'x-company-id': companyid,
        'x-site-ids': siteid,
        
        }

    xnu_url = str(xnu_conn) + "/Staff/Shift/ShiftWorkTime/"
    if debug:
        
        print("Debug: Putting to URL: " + xnu_url)
        print("Debug: Putting with Payload: " + str(json.dumps(data)))
    try:
        res = requests.put( url=xnu_url, data=json.dumps(data), headers=xnu_headers )
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


    return res.status_code

def deleteShifts(xnu_conn, token, companyid, shiftid):
    
    xnu_headers = {
        'content-type': "application/json",
        'cache-control': "no-cache",
        'authorization': token,
        'x-company-id': companyid
        }

    xnu_url = str(xnu_conn) + "/Staff/Shift/" + shiftid
    if debug:
        print("Debug: Deleting shift with ID: " + shiftid)
    try:
        res = requests.request("DELETE", xnu_url,  headers=xnu_headers)
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

    return res.status_code

def getShifts(xnu_conn, token, companyid, siteid):
    
    xnu_headers = {
        'content-type': "application/json",
        'cache-control': "no-cache",
        'authorization': token,
        'x-company-id': companyid,
        'x-site-ids': siteid
        }
    xnu_url = str(xnu_conn) + "/Staff/Shift/"
    if debug:
        print("Calling Staff API to Get Shifts with URL:" + xnu_url)
        print ("Headers: " + str(xnu_headers))
    try:
        res = requests.request("GET", xnu_url,  headers=xnu_headers)
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
    return res.text

def getOnBreakShifts(xnu_conn, token, companyid, siteid):
    xnu_headers = {
        'content-type': "application/json",
        'cache-control': "no-cache",
        'authorization': token,
        'x-company-id': companyid,
        'x-site-ids': siteid
        }
    xnu_url = str(xnu_conn) + "/Staff/Shift/GetBy?itemsPerPage=500&fieldName=Status&value=ON_BREAK"
    if debug:
        print("Calling Staff API to Get Shifts with URL:" + xnu_url)
        print ("Headers: " + str(xnu_headers))
    try:
        res = requests.request("GET", xnu_url,  headers=xnu_headers)
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
    
    return res.text
    
def getOpenShifts(xnu_conn, token, companyid, siteid):
    xnu_headers = {
        'content-type': "application/json",
        'cache-control': "no-cache",
        'authorization': token,
        'x-company-id': companyid,
        'x-site-ids': siteid
        }
    xnu_url = str(xnu_conn) + "/Staff/Shift/GetBy?itemsPerPage=500&fieldName=Status&value=CLOCKED_IN"
    if debug:
        print("Calling Staff API to Get Shifts with URL:" + xnu_url)
        print ("Headers: " + str(xnu_headers))
    try:
        res = requests.request("GET", xnu_url,  headers=xnu_headers)
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

    
    return res.text

def getOpenPunchList(xnu_conn, token, companyid, siteid, start_date, end_date, page_number):
    xnu_headers = {
        'content-type': "application/json",
        'cache-control': "no-cache",
        'authorization': token,
        'x-company-id': companyid,
        'x-site-ids': siteid
        }
    xnu_url = str(xnu_conn) + "/StaffWeb/PunchListItem/GetByPeriod?FieldName%5B0%5D=Status&Value%5B0%5D%5B0%5D=CLOCKED_IN&Value%5B0%5D%5B1%5D=ON_BREAK&FilterAction%5B0%5D=9&SortFieldName=StartDateTime&SortOrder=1&PageNumber=" + page_number + "&ItemsPerPage=100&StartDateTime=" + start_date + "&EndDateTime=" + end_date
    if debug:
        print("Calling Staff API to Get Shifts with URL:" + xnu_url)
        print ("Headers: " + str(xnu_headers))
    try:
        res = requests.request("GET", xnu_url,  headers=xnu_headers)
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
    
    return res.text

def getPunchItem(xnu_conn, token, companyid, siteid, shift_id):
    xnu_headers = {
        'content-type': "application/json",
        'cache-control': "no-cache",
        'authorization': token,
        'x-company-id': companyid,
        'x-site-ids': siteid
        }
    xnu_url = str(xnu_conn) + "/StaffWeb/PunchEditItem/" + shift_id
    if debug:
        print("Calling Staff API to Get Shift Detail with URL:" + xnu_url)
        print ("Headers: " + str(xnu_headers))
    try:
        res = requests.request("GET", xnu_url,  headers=xnu_headers)
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
    
    return res.text


def getShiftDetail(shift_id, xnu_conn, token, companyid, siteid):
    
    xnu_headers = {
        'content-type': "application/json",
        'cache-control': "no-cache",
        'authorization': token,
        'x-company-id': companyid,
        'x-site-ids': siteid
        }
    xnu_url = str(xnu_conn) + "/Staff/ShiftDetail/" + shift_id
    if debug:
        print("Calling Staff API to Get Shift Details with URL:" + xnu_url)
        print ("Headers: " + str(xnu_headers))
    try:
        res = requests.request("GET", xnu_url,  headers=xnu_headers)
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
    return res.text

def putPunchEditItem(xnu_conn, token, companyid, siteid, editJSON):
    
    xnu_headers = {
        'content-type': "application/json",
        'cache-control': "no-cache",
        'authorization': token,
        'x-company-id': companyid,
        'x-site-ids': siteid
        }
    xnu_url = str(xnu_conn) + "/StaffWeb/PunchEditItem/"
    if debug:
        print("Calling StaffWeb API to Put Punch Edit with URL:" + xnu_url)
        print ("Headers: " + str(xnu_headers))
    try:
        res = requests.put( url=xnu_url, data=json.dumps(editJSON), headers=xnu_headers )
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
        print ("ERROR - ANOTHER ISSUE:", e) 
        exit()
    if res.status_code == 200 or res.status_code!=204:
        print("Put Successful for Punch Edit Item - shift_id:" + editJSON["Id"])
    
    return res.text


def postPunchEditItem(xnu_conn, token, companyid, siteid, editJSON):
    xnu_headers = {
        'content-type': "application/json",
        'cache-control': "no-cache",
        'authorization': token,
        'x-company-id': companyid,
        'x-site-ids': siteid
        }
    xnu_url = str(xnu_conn) + "/StaffWeb/PunchEditItem/"
    if debug:
        print("Calling StaffWeb API to Put Punch Edit with URL:" + xnu_url)
        print ("Headers: " + str(xnu_headers))
        print ("Payload: " + str(editJSON))
    try:
        res = requests.post( url=xnu_url, data=json.dumps(editJSON), headers=xnu_headers )
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
    if res.status_code == 200 or res.status_code!=204:
        print("POST Successful for Punch Edit Item.")
    
    return res.text