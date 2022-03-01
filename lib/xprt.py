
import requests, json

debug = 0

#-------------------------------------------------------------------------------
# INTEGRATOR TOKEN
# A token used to Application to Application conversations. 
#-------------------------------------------------------------------------------

def getIntegratorToken(xprtconn, key_id, secret_key, companyid):
    
    itoken_headers = {
        'content-type': "application/json",
        'cache-control': "no-cache"
        }
    itoken_payload = "{\n\n  \"key_id\": \""+ key_id + "\",\n\n  \"secret_key\": \""+ secret_key + "\"\n\n}"
    if debug:
        print("Integrator Token Payload: " + itoken_payload)
    itoken_url = str(xprtconn) + "/integrator/token"
    try:
        res = requests.request("POST", itoken_url, data=itoken_payload, headers=itoken_headers)
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
    if res.status_code != 200:
        print(("ERROR GETTING ACCESS TOKEN: Status Code returned of " + str(res.status_code)))
        exit()
    itoken = res.text
    itoken = "Bearer " + itoken
    if debug:
        print("Token String: " + itoken)
    return itoken
#-------------------------------------------------------------------------------
# PERSON TOKEN
# A person token impersonates a user session. Site access may be restricted
# to the User's list of allowed sites.
#-------------------------------------------------------------------------------
def getPersonToken(xprtconn, user, password):
    authPayload = {
        'user': user,
        'password': password
        }           
    authPayload = json.dumps(authPayload)
   
    authheaders = {
        'content-type': "application/json",
        'cache-control': "no-cache"
        }
    try:
        res = requests.request("POST", xprtconn + "/token", data=authPayload, headers=authheaders)
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
    if res.status_code != 200:
        print(("AUTH ERROR: Problem encountered while getting a person token. Status Code returned of " + str(res.status_code)))
        exit()
    token = res.text
    token = "Bearer " + token
    return token
#-------------------------------------------------------------------------------
# ACCESS TOKEN
# An access token is somewhere in between a Person & Integrator token.
# It's only used in specific portions of the platform, currently.
#-------------------------------------------------------------------------------
def getAccessToken(xprtconn, token, companyid):
    atoken_headers = {
        'authorization': token,
        'content-type': "application/json",
        'cache-control': "no-cache"
        }
    atoken_payload = "{\"company_id\": \"" + companyid + "\"}\n"
    print(atoken_payload)
    accesstokenres = requests.request("POST", xprtconn + "/v1/me/access-token", data=atoken_payload, headers=atoken_headers)
    if accesstokenres.status_code != 200:
        print(("AUTH ERROR: Problem encountered while getting an access token. Status Code returned of " + str(accesstokenres.status_code) + ". Error Description: " + str(accesstokenres.text)))
        exit()
    accesstoken = accesstokenres.text
    accesstoken = "Bearer " + accesstoken
    return accesstoken


#-------------------------------------------------------------------------------
# Get Sites
# Gets a list of Sites for a given Company
#-------------------------------------------------------------------------------
def getSitesForCompany(xprtconn, token, companyid):
    headers = {
        'authorization': token,
        'content-type': "application/json",
        'x-company-id': companyid,
        'cache-control': "no-cache"
        }
    try:
        res = requests.request("GET", xprtconn + "/companies/" + companyid + "/sites",  headers=headers)
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
    if res.status_code != 200:
        print(("AUTH ERROR: Problem encountered while getting the Site List. Status Code returned of " + str(res.status_code) + ". Error Description: " + str(res.text)))
        exit()

    return res.text



#-------------------------------------------------------------------------------
# Get People for Sites
# Gets a list of People related to a given Site
#-------------------------------------------------------------------------------
def getPeopleForSite(xprtconn, token, companyid, siteid):
    headers = {
        'authorization': token,
        'content-type': "application/json",
        'x-company-id': companyid,
        'cache-control': "no-cache"
        }
    try:
        res = requests.request("GET", xprtconn + "/v1/sites/" + siteid + "/people",  headers=headers)
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
    if debug:
        print("GET from " + xprtconn + "/v1/sites/" + siteid + "/people")
    if res.status_code != 200:
        print(("AUTH ERROR: Problem encountered while getting the Site List. Status Code returned of " + str(res.status_code) + ". Error Description: " + str(res.text)))
        exit()

    return res.text