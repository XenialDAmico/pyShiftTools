import requests, json

debug = 0

#-------------------------------------------------------------------------------
# Gets Registry of Xenial URL's
# 
#-------------------------------------------------------------------------------

def getRegistry(environment):
    
    ssr_url = "https://ssr-xenial.heartlandcommerce.com/?env=" + environment
    try:
        res = requests.request("GET", ssr_url)
        if res.status_code != 200:
            print(("ERROR GETTING REGISTRY: Status Code returned of " + str(res.status_code)))
            exit()
        url_list = res.text
    except ConnectionError:
        print(ConnectionError.strerror)
        pass
    return url_list