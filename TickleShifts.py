# Python Version:  3.x 
# Author: Jason D'Amico
# Libraries Required: 
# "Requests" - For more information on installing this lib, see this link:https://pypi.org/project/requests/
# ""
# Sample Usage - Dennys UAT
# python3 TickleShifts.py companyid=61415d24163c350007f029ae  keyid=5cc1128d-18cb-4b00-a38f-342f34729460 secret=db42d23a-9921-44a4-93df-79dbd6f80cae environment=uat siteid=617c11eed44a5d00077d4ade

# !!!!!!!!! The audience for this script is internal to Xenial. !!!!!!!!!!!!!!


import  sys,  json, requests
from datetime import datetime, timedelta
from lib.utils import printProgressBar
from lib.xprt import getSitesForCompany, getIntegratorToken

from lib.ssr import getRegistry
from lib.xnu import getShifts,putShift, getShiftDetail

debug = 1

scriptStart = datetime.now()




# Initialize Variables
companyid = "" 
siteid = "" 
user = ""
password = ""
environment = ""
date=""
secret=""
keyid=""

# -------------------------------------------
# get script arguments
# -------------------------------------------
position = 1
while (position < len(sys.argv)):  
    if "=" in sys.argv[position]:
        KeyValue = sys.argv[position].split("=")
        # Check for 'Environment' Argument
        if KeyValue[0].lower() == 'environment':
            # Get Env from commandline
            environment = KeyValue[1]
            print(("Environment Arg Accepted: " + KeyValue[1]))
        # Check for 'CompanyID' Argument
        elif KeyValue[0].lower() == 'companyid':
            # Get CompanyId from commandline
            companyid = KeyValue[1]
            print(("CompanyId Arg Accepted: " + KeyValue[1]))
        # Check for 'Password' Argument
        elif KeyValue[0].lower() == 'password':
            # Get password from commandline
            password = KeyValue[1]
            print(("Password Arg Accepted: " + KeyValue[1]))
        # Check for 'User' Argument
        elif KeyValue[0].lower() == 'user':
            # Get user from commandline
            user = KeyValue[1]
            print(("User Arg Accepted: " + KeyValue[1]))
        # Check for 'Date' Argument
        elif KeyValue[0].lower() == 'date':
            # Get date from commandline
            date = KeyValue[1]
            print(("Date Arg Accepted: " + KeyValue[1]))
        # Check for 'SiteID' Argument
        elif KeyValue[0].lower() == 'siteid':
            # Get SiteID from commandline
            siteid = KeyValue[1]
            print(("SiteId(s) Arg Accepted: " + KeyValue[1]))
        # Check for 'KeyID' Argument
        elif KeyValue[0].lower() == 'keyid':
            # Get User from commandline
            print(("KeyID Arg Accepted: " + KeyValue[1]))
            keyid = KeyValue[1]
        # Check for 'Secret' Argument
        elif KeyValue[0].lower() == 'secret':
            # Get password from commandline
            secret = KeyValue[1]
            print(("Secret Arg Accepted: " + KeyValue[1]))
    else:
        [KeyValue[0]] = KeyValue[1]
    position += 1
    

# -------------------------------------------
# Setup Environment
# -------------------------------------------

if environment.lower() == "production":
    # Set Defaults
    xprtconn = "https://xprtbackend.heartlandcommerce.com" 
    boconn =  "https://backoffice-api.heartlandcommerce.com"
    rptconn =  "https://reportsbackend.heartlandcommerce.com"

    # Update defaults with values from SSR.
    registry = getRegistry("prod")
    registryJSON = json.loads(registry)
    for url in registryJSON:
        if url["key"].lower == "reporting_api":
            rptconn = url["url"]
    
        if url["key"].lower == "portal":
            xprtconn = url["url"]
    
        if url["key"].lower == "boh_core":
            boconn = url["url"]

if environment.lower() == "qa":
    xprtconn = "https://qa-xprtbackend.xenial.com"
    boconn =  "https://qa-backoffice-api.xenial.com"
    rptconn = "https://qa-reportsbackend.xenial.com"

    # Update defaults from SSR
    registry = getRegistry("prod")
    registryJSON = json.loads(registry)
    for url in registryJSON:
        if url["key"].lower == "reporting_api":
            rptconn = url["url"]
    
        if url["key"].lower == "portal":
            xprtconn = url["url"]
    
        if url["key"].lower == "boh_core":
            boconn = url["url"]

if environment.lower() == "uat":
    xprtconn = "https://uat-xprtbackend.xenial.com"
    boconn =  "https://uat-backoffice-api.xenial.com"
    rptconn = "https://uat-reportsbackend.xenial.com"

    # Update defaults from SSR
    registry = getRegistry("uat")
    registryJSON = json.loads(registry)
    for url in registryJSON:
        if url["key"].lower == "reporting_api":
            rptconn = url["url"]
    
        if url["key"].lower == "portal":
            xprtconn = url["url"]
    
        if url["key"].lower == "boh_core":
            boconn = url["url"]


# Check for a Company - we're not doing much if it's not there.
if companyid.lower() == "" :
    print("FATAL ERROR: Company or Site missing. Pass Argument CompanyID=<value>, and/or SiteID=<value>")
    exit()

# -------------------------------------------
# Main Script Logic - Let's do it!
# -------------------------------------------
today = datetime.today()
todaystr = today.strftime('%Y-%m-%d')
yesterday = today - timedelta(days=1)

yesterdaystr = today.strftime('%Y-%m-%d')

if date =="":
    log_date = today
elif date =="yesterday":
    log_date = yesterday
else:
    log_date = datetime.strptime(todaystr,'%Y-%m-%d')

# Get a token and Authenticate
token = getIntegratorToken(xprtconn, keyid, secret, companyid)

# Get a List of Sites for this Company
sites = getSitesForCompany(xprtconn,token,companyid)
sitesJSON = json.loads(sites)

if siteid:
    # Filter python objects with list comprehensions, down to the site passed into the Arg.
    
    output_dict = [x for x in sitesJSON["items"] if x['id'] == siteid]
    sitesJSON["items"] = output_dict

i = 0

printProgressBar(i, len(sitesJSON["items"]), prefix = 'Progress:', suffix = 'Complete', length = 50)

for  site in sitesJSON["items"]:
        siteStart = datetime.now()
        shifts = getShifts(xnu_conn=boconn,token=token,companyid=companyid, siteid=site["id"])
        
        shiftsJSON = json.loads(shifts)
        if shiftsJSON["TotalCount"] > 0:
            for shift in shiftsJSON["Data"]:
                print(str(shift))
                shift_id = shift["ShiftId"]
                shift_detail = json.loads(getShiftDetail(xnu_conn=boconn, token=token, companyid=companyid, shift_id=shift_id, siteid=site["id"]))
                print(str(shift_detail))
                

                
                putShift(boconn, token, companyid, site["id"], shift_detail)
                print("Tickled shift " + shift_id)
        else:
            print("no shifts to tickle!")
        # Grab Metrics.
        siteEnd = datetime.now()
        duration = siteEnd - siteStart                 
        duration_in_s = duration.total_seconds() 
        print("This site took " + str(duration_in_s) + " to complete.")

scriptEnd = datetime.now()
duration = scriptEnd - scriptStart
duration_in_s = duration.total_seconds()

print("This script is DONE, man.. Fully baked in " + str(duration_in_s) + " seconds.")
