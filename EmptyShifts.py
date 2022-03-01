# Python Version:  3.x 
# Author: Jason D'Amico
# ================================================================================================================================================================
# Libraries Required: 
# "Requests" - For more information on installing this lib, see this link:https://pypi.org/project/requests/
# ================================================================================================================================================================
# Sample Usage - Dennys UAT
# python3 EmptyShifts.py companyid=61415d24163c350007f029ae  keyid=5cc1128d-18cb-4b00-a38f-342f34729460 secret=db42d23a-9921-44a4-93df-79dbd6f80cae environment=uat 

# ========================================================================================================================================================================================================

# !!!!!!!!! The audience for this script is internal to Xenial. Do NOT share with customers. !!!!!!!!!!!!!!


import  sys,  json, requests
from datetime import datetime, timedelta
from lib.utils import logError,logInfo,logWarning, printProgressBar
from lib.xprt import getSitesForCompany, getIntegratorToken

from lib.ssr import getRegistry
from lib.xnu import deleteShifts, getOpenShifts, getShiftDetail

from pprint import pprint

debug = 0
deleteEmptyShifts = 0

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
        # Check for 'DeleteShifts' Argument
        elif KeyValue[0].lower() == 'deleteemptyshifts':
            # Get SiteID from commandline
            deleteEmptyShifts = KeyValue[1]
            print(("deleteEmptyShifts Arg Accepted: " + KeyValue[1]))
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

emptyShifts = []
for  site in sitesJSON["items"]:

        siteStart = datetime.now()
        # Get all Shifts with a Clock Status of "Clocked In" (Additional Research on this Endpoint may be needed. Sometimes "extra" records seem to be returned.)
        shiftsJSON = json.loads(getOpenShifts(xnu_conn=boconn,token=token,companyid=companyid, siteid=site["id"]))
        
        if shiftsJSON["TotalCount"] > 0:
            for shift in shiftsJSON["Data"]:
                shiftid = shift["ShiftId"]
                
                # Get the details for shifts in the Open Shift list.
                shift_details_json = json.loads(getShiftDetail(shiftid, xnu_conn=boconn,token=token,companyid=companyid, siteid=site["id"]))
                if debug:
                    pprint(shift_details_json)
                # If the EmployeeWorkTimes array is empty, this shift is bullshit, since its nonsensicle clocked in without a work time record.
                if len(shift_details_json["EmployeeWorkTimes"]) == 0:
                    print("Found an Empty shift with id:" + shiftid)
                    print("Shift Start:" + shift["StartDateTime"])
                     
                    

                    # Append the rogue shift to this array, it'll be be useful later.
                    emptyShifts.append(shift_details_json)
                    
                    # Try saying the above sentence 10 times fast. Impossible.
                    if str(deleteEmptyShifts)=="1":
                        print("Deleting Empty Shift with ID: " + shiftid)
                        deleteShifts(shiftid=shiftid, xnu_conn=boconn,token=token,companyid=companyid)
                   
                    else:
                        if debug:
                            print("Skipping shift deletion. Pass in deleteEmptyShifts=1 to Delete this empty Shift.")

        # Grab Metrics.
        siteEnd = datetime.now()
        duration = siteEnd - siteStart                 
        duration_in_s = duration.total_seconds() 
        print("Site ID: " + site["id"] + " took " + str(duration_in_s) + "s to check. Number of Open Shifts Found: " + str(len(shiftsJSON["Data"])) + ". Current count of problematic shifts: " + str(len(emptyShifts)))
        
        i = i + 1
        printProgressBar(i, len(sitesJSON["items"]), prefix = 'Progress:', suffix = 'Complete', length = 50)

scriptEnd = datetime.now()
duration = scriptEnd - scriptStart
duration_in_s = duration.total_seconds()
print("This script is DONE, man.. Fully baked in " + str(duration_in_s) + " seconds.")
if len(emptyShifts)==0:
    print("No problematic shifts were found for the provided company and/or site.")
else:
    print("Problematic Shifts were found:")
    pprint(emptyShifts)
