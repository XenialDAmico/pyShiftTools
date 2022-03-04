# Split shifts at the time designated as the Payroll Cutover in DM (Staff--> Business Rules)
# Python Version:  3.x 
# Author: Jason D'Amico
# ================================================================================================================================================================
# Libraries Required: 
# "Requests" - For more information on installing this lib, see this link:https://pypi.org/project/requests/
# ================================================================================================================================================================
# Sample Usage - Dennys UAT
# python3 SplitShifts.py companyid=61415d24163c350007f029ae  keyid=5cc1128d-18cb-4b00-a38f-342f34729460 secret=db42d23a-9921-44a4-93df-79dbd6f80cae environment=uat siteid=617c11eed44a5d00077d4ade
#
# Sample Usage - Dennys Prod
# python3 SplitShifts.py siteid=60107930fc8b6e00078d6862 companyid=5ddab0e3d93109001df6a76c keyid=ac5515b8-269d-481e-8af3-c5b57f9cca3d secret=f1e6f1eb-0c3b-4d60-b472-11be6649ef3d environment=production 

# Sample - Dennys (QA) 
# python3 SplitShifts.py companyid=6141ac6e3434d8000716f5fb  keyid=7568f581-eb4f-4f9e-8c6f-22a258226714 secret=daf4cd7b-4ba5-4417-9684-2e879390490c environment=qa siteid=6141ac8de2d8a9000828a0a0
# ========================================================================================================================================================================================================

# !!!!!!!!! The audience for this script is internal to Xenial. Do NOT share with customers. !!!!!!!!!!!!!!

# TO DO LIST:
# Get Offset from Portal (sites). Currently, this script will only work for sites in the east coast



import  sys,  json, requests, pytz, logging, time

from datetime import datetime, timedelta
from lib.utils import  printProgressBar,log
from lib.xprt import getSitesForCompany, getIntegratorToken

from lib.ssr import getRegistry
from lib.xnu import getOnBreakShifts, getOpenPunchList, getPunchItem, putPunchEditItem, postPunchEditItem
from lib.dm import getPayrollCutoverTime

from pprint import pprint


utc=pytz.UTC

debug = 0

def main():
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
                log("INFO","Environment Arg Accepted: " + KeyValue[1])
            # Check for 'CompanyID' Argument
            elif KeyValue[0].lower() == 'companyid':
                # Get CompanyId from commandline
                companyid = KeyValue[1]
                log("INFO","CompanyId Arg Accepted: " + KeyValue[1])
            # Check for 'SiteID' Argument
            elif KeyValue[0].lower() == 'siteid':
                # Get SiteID from commandline
                siteid = KeyValue[1]
                log("INFO","SiteId(s) Arg Accepted: " + KeyValue[1])
            # Check for 'KeyID' Argument
            elif KeyValue[0].lower() == 'keyid':
                # Get User from commandline
                log("INFO","KeyID Arg Accepted: " + KeyValue[1])
                keyid = KeyValue[1]
            # Check for 'Secret' Argument
            elif KeyValue[0].lower() == 'secret':
                # Get password from commandline
                secret = KeyValue[1]
                log("INFO","Secret Arg Accepted: " + KeyValue[1])
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
        dmconn = "https://dmbackend.heartlandcommerce.com"

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
        dmconn = "https://qa-dmbackend.heartlandcommerce.com"

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
            if url["key"].lower == "dm":
                dmconn = url["url"]

    if environment.lower() == "uat":
        xprtconn = "https://uat-xprtbackend.xenial.com"
        boconn =  "https://uat-green-backoffice-api-us-east-1.xenial.com"
        rptconn = "https://uat-reportsbackend.xenial.com"
        dmconn = "https://uat-green-dmbackend-us-east-1.xenial.com"
        

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
            if url["key"].lower == "dm":
                dmconn = url["url"]


    # Check for a Company - we're not doing much if it's not there.
    if companyid.lower() == "" :
        print("FATAL ERROR: Company or Site missing. Pass Argument CompanyID=<value>, and/or SiteID=<value>")
        log("ERROR","FATAL ERROR: Company or Site missing. Pass Argument CompanyID=<value>, and/or SiteID=<value>")
        exit(1)

    # -------------------------------------------
    # Main Script Logic - Let's do it!
    # -------------------------------------------
    today = datetime.today()
    today = today.replace(tzinfo=utc)
    todaystr = today.strftime('%Y-%m-%d')
    yesterday = today - timedelta(days=1)
    yesterdaystr = yesterday.strftime('%Y-%m-%d')
    lastweek = today - timedelta(days=7)
    lastweekstr = lastweek.strftime('%Y-%m-%d')


    # Get a token and Authenticate
    token = getIntegratorToken(xprtconn, keyid, secret, companyid)

    # Get a List of Sites for this Company
    sites = getSitesForCompany(xprtconn,token,companyid)
    sitesJSON = json.loads(sites)

    if siteid:
        # Filter python objects with list comprehensions, down to the site passed into the Arg.
        output_dict = [x for x in sitesJSON["items"] if x['id'] == siteid]
        sitesJSON["items"] = output_dict

    # Progress is a nice touch, perhaps...
    i = 0
    printProgressBar(i, len(sitesJSON["items"]), prefix = 'Progress:', suffix = 'Complete', length = 50)
    for  site in sitesJSON["items"]:
            siteStart = datetime.now()
            log("INFO", "Starting loop for Site ID: " + str(site["id"]))

            #Set Default Value, but override with settings from DM.
            punch_search_end_date_string = todaystr + "T06:59:00"
            punch_search_start_date_string  = lastweekstr + "T00:00:00"

            payroll_cutover_string = getPayrollCutoverTime(dmconn,token,companyid,site["id"])
            log("INFO", "Payroll Cutover Time String from DM reflects value of '" + payroll_cutover_string + "'.")
            

            payroll_cutover_time = datetime.strptime(payroll_cutover_string[0:5], '%H:%M')
            log("INFO", "Interpreted this string as Payroll Cutover Time of '" + str(payroll_cutover_time) + "'.")

            punch_search_end_dt = payroll_cutover_time - timedelta(seconds=1)
            punch_search_end_date_string = todaystr + "T" + datetime.strftime(punch_search_end_dt,'%H:%M:%S') 
            
        
           
            # Get all Shifts with a Clock Status of "Clocked In" & "On Break"
            openshiftsJSON = json.loads(getOpenPunchList(xnu_conn=boconn,token=token,companyid=companyid, siteid=site["id"],start_date=punch_search_start_date_string,end_date=punch_search_end_date_string,page_number="0"))
            if debug:
                log("INFO", "Open Punch List JSON:" + str(openshiftsJSON))
            if openshiftsJSON["TotalCount"] > 0:
                for shift in openshiftsJSON["Data"]:
                    put_item = {
                                            
                                            "EmployeeId": "",
                                            "EmployeeJobId": "",
                                            "ClockIn": "",
                                            "ClockOut": "",
                                            "Breaks": [],
                                            "Tips": [],
                                            "Source": "EOD Split Punch",
                                            "AdjustmentReasonId": "58f66d487024f950c17c3e63",
                                            "AdjustmentNote": "End of Day"
                                            }
                    post_item = {
                                            "EmployeeId": "",
                                            "EmployeeJobId": "",
                                            "ClockIn": "",
                                            "ClockOut": None,
                                            "Breaks": [],
                                            "Tips": [],
                                            "Source": "EOD Split Punch",
                                            "AdjustmentReasonId": "58f66d487024f950c17c3e63"
                                            }
                    shift_id = shift["Id"]
                    
                    log("INFO","Open Shift Object: " + str(shift))
                    break_count = int(shift["Breaks"])
                    log("INFO","Break Count for Shift (" + shift["Id"] + ") is " + str(break_count))
                    status = str(shift["Status"])
                    # Get the details for shifts in the Open Shift list.
                    shift_details_json = json.loads(getPunchItem(xnu_conn=boconn,token=token,companyid=companyid, siteid=site["id"], shift_id = shift_id))
                    
                    
                    

                    #Let's check to see if this Shift was already split, based on a 7:00AM start time
                    ClockinDate = datetime. strptime(shift_details_json["Model"]["ClockIn"], '%Y-%m-%dT%H:%M:%S%z')
                    if ClockinDate.strftime('%H:%M') == datetime.strftime(payroll_cutover_time,'%H:%M'):
                        if debug:
                            print("Skipping Previously Split Record!")
                        log("INFO","Skipping the following previously split shift: " + json.dumps(shift_details_json))
                        
                        continue

                    #Also, if Clock In is after 7:00AM, we dont want to touch this shift either.

                    today_dt=todaystr + "T" + datetime.strftime(payroll_cutover_time,'%H:%M') + ":01-05:00"
                    if ClockinDate >= datetime. strptime(today_dt, '%Y-%m-%dT%H:%M:%S%z'):
                        log("INFO","Skipping the following shift for the current day: " + json.dumps(shift_details_json))
                        continue

                    if break_count == 0:
                        shift_start = shift_details_json["Model"]["ClockIn"] 
                        shift_end = todaystr + "T" + datetime.strftime(payroll_cutover_time,'%H:%M') + ":00-05:00"

                        put_item["EmployeeId"]=shift_details_json["Model"]["EmployeeId"] 
                        put_item["EmployeeJobId"]=shift_details_json["Model"]["EmployeeJobId"] 
                        put_item["ClockIn"]=shift_details_json["Model"]["ClockIn"] 
                        put_item["ClockOut"]=shift_end
                        put_item["Id"]=shift_details_json["Model"]["Id"] 

                        put_item_json = json.loads(json.dumps(put_item))

                        log("INFO","Creating new Punch without any Break Time ")
                        log("INFO",put_item_json)

                        putPunchEditItem(xnu_conn = boconn,token=token,companyid=companyid,siteid=site["id"], editJSON=put_item_json)

                        # Post a new Punch Edit one second after the end of the previous.
                        post_item["EmployeeId"]=shift_details_json["Model"]["EmployeeId"] 
                        post_item["EmployeeJobId"]=shift_details_json["Model"]["EmployeeJobId"] 
                        post_item["ClockIn"]=todaystr + "T07:00:01-05:00"
                        post_item_json = json.loads(json.dumps(post_item))

                        log("INFO","Creating new Punch without any Break Time")
                        log("INFO",post_item_json)

                        postPunchEditItem(xnu_conn = boconn,token=token,companyid=companyid,siteid=site["id"], editJSON=post_item_json)

                    elif break_count > 0 and status == "CLOCKED_IN":
                        shift_start = shift_details_json["Model"]["ClockIn"] 
                        # Fix this when you implement method to retrieve Offset from Portal
                        shift_end = todaystr + "T" + datetime.strftime(payroll_cutover_time,'%H:%M') + ":00-05:00"

                        put_item["EmployeeId"]=shift_details_json["Model"]["EmployeeId"] 
                        put_item["EmployeeJobId"]=shift_details_json["Model"]["EmployeeJobId"] 
                        put_item["ClockIn"]=shift_details_json["Model"]["ClockIn"] 
                        put_item["ClockOut"]=shift_end
                        put_item["Id"]=shift_details_json["Model"]["Id"] 
                        break_list = []
                        for brk in shift_details_json["Model"]["Breaks"]:
                            if debug:
                                pprint("Break:" + str(brk))
                            
                            # Look for break with empty end time. Replace empty time with Payroll cutover time
                            if brk["EndDateTime"] != None:
                                break_list.append({"startDateTime": brk["StartDateTime"], "endDateTime": brk["EndDateTime"], "BreakTimeId": brk["BreakTimeId"]})
                            # If Break is Completed, append it to the list.
                            else:
                                break_list.append({"StartDateTime": brk["StartDateTime"], "EndDateTime": shift_end, "BreakTimeId": brk["BreakTimeId"]})
                                
                        put_item["Breaks"] = break_list        
                        put_item_json = json.loads(json.dumps(put_item))

                        log("INFO","Creating new Punch with Break Time")
                        log("INFO",put_item_json)
                        putPunchEditItem(xnu_conn = boconn,token=token,companyid=companyid,siteid=site["id"], editJSON=put_item_json)
                        
                        # Post a new Punch Edit one second after the end of the previous.
                        post_item["EmployeeId"]=shift_details_json["Model"]["EmployeeId"] 
                        post_item["EmployeeJobId"]=shift_details_json["Model"]["EmployeeJobId"] 
                        post_item["ClockIn"]=todaystr  + "T" + datetime.strftime(payroll_cutover_time,'%H:%M') + ":01-05:00"
                        
                        post_item_json = json.loads(json.dumps(post_item))

                        log("INFO","Creating new Punch without any Break Time for Employee " + employee_name)
                        log("INFO",post_item_json)

                        postPunchEditItem(xnu_conn = boconn,token=token,companyid=companyid,siteid=site["id"], editJSON=post_item_json)
                    else:
                        shift_start = shift_details_json["Model"]["ClockIn"] 
                        # Fix this when you implement method to retrieve Payroll Cutover from DM.
                        shift_end = todaystr + "T" + datetime.strftime(payroll_cutover_time,'%H:%M') + ":00-05:00"

                        put_item["EmployeeId"]=shift_details_json["Model"]["EmployeeId"] 
                        put_item["EmployeeJobId"]=shift_details_json["Model"]["EmployeeJobId"] 
                        put_item["ClockIn"]=shift_details_json["Model"]["ClockIn"] 
                        put_item["ClockOut"]=shift_end
                        put_item["Id"]=shift_details_json["Model"]["Id"] 
                        break_list = []
                        for brk in shift_details_json["Model"]["Breaks"]:
                            if debug:
                                pprint("Break:" + str(brk))
                            
                            # Look for break with empty end time. Replace empty time with Payroll cutover time
                            if brk["EndDateTime"] != None:
                                break_list.append({"startDateTime": brk["StartDateTime"], "endDateTime": brk["EndDateTime"], "BreakTimeId": brk["BreakTimeId"]})
                            # If Break is Completed, append it to the list.
                            else:
                                break_list.append({"StartDateTime": brk["StartDateTime"], "EndDateTime": shift_end, "BreakTimeId": brk["BreakTimeId"]})
                                
                        put_item["Breaks"] = break_list        
                        put_item_json = json.loads(json.dumps(put_item))
                        
                        log("INFO","Creating new Punch with Break Time: ")
                        log("INFO",put_item_json)

                        putPunchEditItem(xnu_conn = boconn,token=token,companyid=companyid,siteid=site["id"], editJSON=put_item_json)
                        
                        # Post a new Punch Edit one second after the end of the previous.
                        post_item["EmployeeId"]=shift_details_json["Model"]["EmployeeId"] 
                        post_item["EmployeeJobId"]=shift_details_json["Model"]["EmployeeJobId"] 
                        post_item["ClockIn"]=todaystr  + "T" + datetime.strftime(payroll_cutover_time,'%H:%M') + ":01-05:00"
                        break_list=[]
                        break_list.append({"StartDateTime": todaystr + "T" + datetime.strftime(payroll_cutover_time,'%H:%M') + ":01-05:00", "EndDateTime": None, "BreakTimeId": brk["BreakTimeId"]})
                        
                        post_item["Breaks"] = break_list  
                        post_item_json = json.loads(json.dumps(post_item))

                        log("INFO","Creating new Punch without any Break Time: ")
                        log("INFO",post_item_json)
                        postPunchEditItem(xnu_conn = boconn,token=token,companyid=companyid,siteid=site["id"], editJSON=post_item_json)
                        
            # Grab Metrics.
            siteEnd = datetime.now()
            duration = siteEnd - siteStart                 
            duration_in_s = duration.total_seconds() 
            print("Site ID: " + site["id"] + " took " + str(duration_in_s) + "s to check. Number of Open Shifts Found: " + str(len(openshiftsJSON["Data"]))  )
            
            i = i + 1
            printProgressBar(i, len(sitesJSON["items"]), prefix = 'Progress:', suffix = 'Complete', length = 50)

    scriptEnd = datetime.now()
    duration = scriptEnd - scriptStart
    duration_in_s = duration.total_seconds()
    log("INFO","This script is DONE, man.. Fully baked in " + str(duration_in_s) + " seconds.")
    exit(0)

if __name__ == "__main__":
    main()