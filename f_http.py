#================================================
# Modules
#================================================
import requests
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
import json
import os
from configparser import ConfigParser
#================================================
# Functions
#================================================
def http_get(url, token, ssl_verify=False ):
    # response 200
    AS_QUERY_PARAM = '?api-token='+ token
    url = url
    #print(url)
    headers = {
        'Content-Type' : 'application/json',
        "accept" : "application/json",
        "charset" : "utf-8",
        "Authorization" : "Api-Token " + token ,
        #'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
        #'Cookie' : '_gcl_au=1.1.672628857.1597240908; _ft_info=%7B%22utm_campaign%22%3A%22none%22%2C%22utm_content%22%3A%22none%22%2C%22utm_medium%22%3A%22website%22%2C%22utm_source%22%3A%22organic%22%2C%22utm_term%22%3A%22none%22%2C%22vehicle_name%22%3A%22none%22%2C%22landingpage%22%3A%22https%3A//www.dynatrace.com/news/category/product-news/%22%2C%22original_referrer%22%3A%22none%22%7D; prexisthb=%7B%22utm_campaign%22%3A%22none%22%2C%22utm_content%22%3A%22none%22%2C%22utm_medium%22%3A%22website%22%2C%22utm_source%22%3A%22organic%22%2C%22utm_term%22%3A%22none%22%2C%22vehicle_name%22%3A%22none%22%2C%22landingpage%22%3A%22https%3A//www.dynatrace.com/news/category/product-news/%22%2C%22original_referrer%22%3A%22none%22%7D; _ga=GA1.2.593057164.1597240915; _mkto_trk=id:352-NVO-562&token:_mch-dynatrace.com-1597240915260-75640; _fbp=fb.1.1597240915799.1453774814; p23mn32t=TH23TSF6DAH6JBQV525GCDE7OQ; _vwo_uuid_v2=D0EFA74BC8C40319699907DFAD2ADFF7F|a5ed6179c5987dbcc7b5bf20f4a962a7; _vis_opt_s=1%7C; _vwo_uuid=D0EFA74BC8C40319699907DFAD2ADFF7F; _vwo_ds=3%241598451425%3A29.14773939%3A%3A; _rxt_cookiepolicy=1; rxVisitor=1597240906752ACLSA5Q0NLKI25PQ9GU0RAS2CUFBF064; _gid=GA1.2.559498932.1600674009; rxsession==3=srv=4=sn=F9CA8486E793B8412DAE4CF019E57602=perc=100000=ol=0=mul=1=app:7fb64fd3b202c513=1=app:366f9fc79607e4b1=1; b925d32c=QX4I5CYD6B3I5CG2FL3OMHK5FE; ssoCSRFCookie=8d6c8371511e6fefd2079d10bb0f872333848efd862e37fe7ab9031de0d51f7e; JSESSIONID=E176177E8027AC86933F5866272B4653; apmsessionid=node01rxljisckl3jg1s53j73b7wjq6468.node0; dtSa=-; rxpc=4$502150672_195h-vKSCMKMDUFSTOHTVNMGDHJAEFCFUQKWUF-0e5; rxlatency=1; dtLatC=1; dtCookie=4$HGDM0E9GKCRC8CCD7LVKPELF6VR0D2AH|fff1ee41ce05f800|1|9a85821213a24845|1|1bc3b8a52b571c99|1|ac58787e2e32ae53|1|8bc7ac3ff70c4079|1; intercom-session-emeshyeu=V3JMSk9DSEtOejVRSGJWRklaQmh1UUlDSDRJTGxjME5PVWJPK2JSQ3dOTnZ2cVdOL3FRS3NmWFdXamd1K1JNRC0tTzM5Y09KZVhMZVM1aXZhNlFpUFJ0dz09--2c592fb3564672638b7e8c515577041d19ff4cd8; dtPC=2$503247007_880h3vPFAPDDCMSSTPCHTIBKAAAUUTMEQHRFCH-2e48; dtCookie=v_4_srv_36_sn_HGDM0E9GKCRC8CCD7LVKPELF6VR0D2AH_perc_100000_ol_0_mul_1_app-3Afff1ee41ce05f800_1_app-3A9a85821213a24845_1_app-3A1bc3b8a52b571c99_1_app-3Aac58787e2e32ae53_1_app-3A8bc7ac3ff70c4079_1; rxvt=1600705074840|1600701358805',
        'Api-Token' : token
    }
    #print(headers)
    r = requests.get( url ,verify=ssl_verify, headers=headers )
    #print("Response size:")
    #print(len(r.content)/1000)
    if ( r.status_code != 200 ):
        msg = 'Error! code=' + str(r.status_code) + ', content=' + r.text
        err = True

    else:
        msg = json.dumps(r.json(), indent=4, sort_keys=True)
        err = False
    
    return err, msg

def http_get_script(url, token, ssl_verify=False ):
    # response 200
    AS_QUERY_PARAM = '?api-token='+ token
    url = url
    #print(url)
    headers = {
        'accept': 'text/plain; charset=utf-8',
        "Authorization" : "Api-Token " + token ,
        #'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
        #'Cookie' : '_gcl_au=1.1.672628857.1597240908; _ft_info=%7B%22utm_campaign%22%3A%22none%22%2C%22utm_content%22%3A%22none%22%2C%22utm_medium%22%3A%22website%22%2C%22utm_source%22%3A%22organic%22%2C%22utm_term%22%3A%22none%22%2C%22vehicle_name%22%3A%22none%22%2C%22landingpage%22%3A%22https%3A//www.dynatrace.com/news/category/product-news/%22%2C%22original_referrer%22%3A%22none%22%7D; prexisthb=%7B%22utm_campaign%22%3A%22none%22%2C%22utm_content%22%3A%22none%22%2C%22utm_medium%22%3A%22website%22%2C%22utm_source%22%3A%22organic%22%2C%22utm_term%22%3A%22none%22%2C%22vehicle_name%22%3A%22none%22%2C%22landingpage%22%3A%22https%3A//www.dynatrace.com/news/category/product-news/%22%2C%22original_referrer%22%3A%22none%22%7D; _ga=GA1.2.593057164.1597240915; _mkto_trk=id:352-NVO-562&token:_mch-dynatrace.com-1597240915260-75640; _fbp=fb.1.1597240915799.1453774814; p23mn32t=TH23TSF6DAH6JBQV525GCDE7OQ; _vwo_uuid_v2=D0EFA74BC8C40319699907DFAD2ADFF7F|a5ed6179c5987dbcc7b5bf20f4a962a7; _vis_opt_s=1%7C; _vwo_uuid=D0EFA74BC8C40319699907DFAD2ADFF7F; _vwo_ds=3%241598451425%3A29.14773939%3A%3A; _rxt_cookiepolicy=1; rxVisitor=1597240906752ACLSA5Q0NLKI25PQ9GU0RAS2CUFBF064; _gid=GA1.2.559498932.1600674009; rxsession==3=srv=4=sn=F9CA8486E793B8412DAE4CF019E57602=perc=100000=ol=0=mul=1=app:7fb64fd3b202c513=1=app:366f9fc79607e4b1=1; b925d32c=QX4I5CYD6B3I5CG2FL3OMHK5FE; ssoCSRFCookie=8d6c8371511e6fefd2079d10bb0f872333848efd862e37fe7ab9031de0d51f7e; JSESSIONID=E176177E8027AC86933F5866272B4653; apmsessionid=node01rxljisckl3jg1s53j73b7wjq6468.node0; dtSa=-; rxpc=4$502150672_195h-vKSCMKMDUFSTOHTVNMGDHJAEFCFUQKWUF-0e5; rxlatency=1; dtLatC=1; dtCookie=4$HGDM0E9GKCRC8CCD7LVKPELF6VR0D2AH|fff1ee41ce05f800|1|9a85821213a24845|1|1bc3b8a52b571c99|1|ac58787e2e32ae53|1|8bc7ac3ff70c4079|1; intercom-session-emeshyeu=V3JMSk9DSEtOejVRSGJWRklaQmh1UUlDSDRJTGxjME5PVWJPK2JSQ3dOTnZ2cVdOL3FRS3NmWFdXamd1K1JNRC0tTzM5Y09KZVhMZVM1aXZhNlFpUFJ0dz09--2c592fb3564672638b7e8c515577041d19ff4cd8; dtPC=2$503247007_880h3vPFAPDDCMSSTPCHTIBKAAAUUTMEQHRFCH-2e48; dtCookie=v_4_srv_36_sn_HGDM0E9GKCRC8CCD7LVKPELF6VR0D2AH_perc_100000_ol_0_mul_1_app-3Afff1ee41ce05f800_1_app-3A9a85821213a24845_1_app-3A1bc3b8a52b571c99_1_app-3Aac58787e2e32ae53_1_app-3A8bc7ac3ff70c4079_1; rxvt=1600705074840|1600701358805',
        'Api-Token' : token
    }
    #print(headers)
    r = requests.get( url ,verify=ssl_verify, headers=headers )
    #print("Response size:")
    #print(len(r.content)/1000)

    if ( r.status_code != 200 ):
        msg = 'Error! code=' + str(r.status_code) + ', content=' + r.text
        err = True

    else:
        msg = r.content#json.dumps(r.json(), indent=4, sort_keys=True)
        err = False
    
    return err, msg

## POST ##
def http_post(url, token, data, ssl_verify=False):
    # response 201
    payload = json.dumps(data, indent=4)
    headers = {
        "accept" : "application/json",
        "charset" : "utf-8",
        "Authorization" : "Api-Token " + token ,
        'Content-Type': "application/json",
        'Cache-Control': "no-cache",
        'Accept-Encoding': "gzip, deflate",
        'Connection': "keep-alive",
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
        'Cookie' : '_gcl_au=1.1.672628857.1597240908; _ft_info=%7B%22utm_campaign%22%3A%22none%22%2C%22utm_content%22%3A%22none%22%2C%22utm_medium%22%3A%22website%22%2C%22utm_source%22%3A%22organic%22%2C%22utm_term%22%3A%22none%22%2C%22vehicle_name%22%3A%22none%22%2C%22landingpage%22%3A%22https%3A//www.dynatrace.com/news/category/product-news/%22%2C%22original_referrer%22%3A%22none%22%7D; prexisthb=%7B%22utm_campaign%22%3A%22none%22%2C%22utm_content%22%3A%22none%22%2C%22utm_medium%22%3A%22website%22%2C%22utm_source%22%3A%22organic%22%2C%22utm_term%22%3A%22none%22%2C%22vehicle_name%22%3A%22none%22%2C%22landingpage%22%3A%22https%3A//www.dynatrace.com/news/category/product-news/%22%2C%22original_referrer%22%3A%22none%22%7D; _ga=GA1.2.593057164.1597240915; _mkto_trk=id:352-NVO-562&token:_mch-dynatrace.com-1597240915260-75640; _fbp=fb.1.1597240915799.1453774814; p23mn32t=TH23TSF6DAH6JBQV525GCDE7OQ; _vwo_uuid_v2=D0EFA74BC8C40319699907DFAD2ADFF7F|a5ed6179c5987dbcc7b5bf20f4a962a7; _vis_opt_s=1%7C; _vwo_uuid=D0EFA74BC8C40319699907DFAD2ADFF7F; _vwo_ds=3%241598451425%3A29.14773939%3A%3A; _rxt_cookiepolicy=1; rxVisitor=1597240906752ACLSA5Q0NLKI25PQ9GU0RAS2CUFBF064; _gid=GA1.2.559498932.1600674009; rxsession==3=srv=4=sn=F9CA8486E793B8412DAE4CF019E57602=perc=100000=ol=0=mul=1=app:7fb64fd3b202c513=1=app:366f9fc79607e4b1=1; b925d32c=QX4I5CYD6B3I5CG2FL3OMHK5FE; ssoCSRFCookie=8d6c8371511e6fefd2079d10bb0f872333848efd862e37fe7ab9031de0d51f7e; JSESSIONID=E176177E8027AC86933F5866272B4653; apmsessionid=node01rxljisckl3jg1s53j73b7wjq6468.node0; dtSa=-; rxpc=4$502150672_195h-vKSCMKMDUFSTOHTVNMGDHJAEFCFUQKWUF-0e5; rxlatency=1; dtLatC=1; dtCookie=4$HGDM0E9GKCRC8CCD7LVKPELF6VR0D2AH|fff1ee41ce05f800|1|9a85821213a24845|1|1bc3b8a52b571c99|1|ac58787e2e32ae53|1|8bc7ac3ff70c4079|1; intercom-session-emeshyeu=V3JMSk9DSEtOejVRSGJWRklaQmh1UUlDSDRJTGxjME5PVWJPK2JSQ3dOTnZ2cVdOL3FRS3NmWFdXamd1K1JNRC0tTzM5Y09KZVhMZVM1aXZhNlFpUFJ0dz09--2c592fb3564672638b7e8c515577041d19ff4cd8; dtPC=2$503247007_880h3vPFAPDDCMSSTPCHTIBKAAAUUTMEQHRFCH-2e48; dtCookie=v_4_srv_36_sn_HGDM0E9GKCRC8CCD7LVKPELF6VR0D2AH_perc_100000_ol_0_mul_1_app-3Afff1ee41ce05f800_1_app-3A9a85821213a24845_1_app-3A1bc3b8a52b571c99_1_app-3Aac58787e2e32ae53_1_app-3A8bc7ac3ff70c4079_1; rxvt=1600705074840|1600701358805'
    }
    r = requests.post( url ,verify=ssl_verify, headers=headers, data=payload )
    if ( r.status_code not in [200, 201, 204] ):
        msg = 'Error! code=' + str(r.status_code) + ', content=' + r.text
        err = True
    else:
        if ( r.status_code == 204 ):
            msg = 'OK ' + str(r.status_code)
        else:
            msg = r.text
        err = False
    return err, msg

def http_post(url, token, ssl_verify=False):
    # response 201
    #payload = json.dumps(data, indent=4)
    headers = {
        "accept" : "application/json",
        "charset" : "utf-8",
        "Authorization" : "Api-Token " + token ,
        'Content-Type': "application/json",
        'Cache-Control': "no-cache",
        'Accept-Encoding': "gzip, deflate",
        'Connection': "keep-alive",
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
        'Cookie' : '_gcl_au=1.1.672628857.1597240908; _ft_info=%7B%22utm_campaign%22%3A%22none%22%2C%22utm_content%22%3A%22none%22%2C%22utm_medium%22%3A%22website%22%2C%22utm_source%22%3A%22organic%22%2C%22utm_term%22%3A%22none%22%2C%22vehicle_name%22%3A%22none%22%2C%22landingpage%22%3A%22https%3A//www.dynatrace.com/news/category/product-news/%22%2C%22original_referrer%22%3A%22none%22%7D; prexisthb=%7B%22utm_campaign%22%3A%22none%22%2C%22utm_content%22%3A%22none%22%2C%22utm_medium%22%3A%22website%22%2C%22utm_source%22%3A%22organic%22%2C%22utm_term%22%3A%22none%22%2C%22vehicle_name%22%3A%22none%22%2C%22landingpage%22%3A%22https%3A//www.dynatrace.com/news/category/product-news/%22%2C%22original_referrer%22%3A%22none%22%7D; _ga=GA1.2.593057164.1597240915; _mkto_trk=id:352-NVO-562&token:_mch-dynatrace.com-1597240915260-75640; _fbp=fb.1.1597240915799.1453774814; p23mn32t=TH23TSF6DAH6JBQV525GCDE7OQ; _vwo_uuid_v2=D0EFA74BC8C40319699907DFAD2ADFF7F|a5ed6179c5987dbcc7b5bf20f4a962a7; _vis_opt_s=1%7C; _vwo_uuid=D0EFA74BC8C40319699907DFAD2ADFF7F; _vwo_ds=3%241598451425%3A29.14773939%3A%3A; _rxt_cookiepolicy=1; rxVisitor=1597240906752ACLSA5Q0NLKI25PQ9GU0RAS2CUFBF064; _gid=GA1.2.559498932.1600674009; rxsession==3=srv=4=sn=F9CA8486E793B8412DAE4CF019E57602=perc=100000=ol=0=mul=1=app:7fb64fd3b202c513=1=app:366f9fc79607e4b1=1; b925d32c=QX4I5CYD6B3I5CG2FL3OMHK5FE; ssoCSRFCookie=8d6c8371511e6fefd2079d10bb0f872333848efd862e37fe7ab9031de0d51f7e; JSESSIONID=E176177E8027AC86933F5866272B4653; apmsessionid=node01rxljisckl3jg1s53j73b7wjq6468.node0; dtSa=-; rxpc=4$502150672_195h-vKSCMKMDUFSTOHTVNMGDHJAEFCFUQKWUF-0e5; rxlatency=1; dtLatC=1; dtCookie=4$HGDM0E9GKCRC8CCD7LVKPELF6VR0D2AH|fff1ee41ce05f800|1|9a85821213a24845|1|1bc3b8a52b571c99|1|ac58787e2e32ae53|1|8bc7ac3ff70c4079|1; intercom-session-emeshyeu=V3JMSk9DSEtOejVRSGJWRklaQmh1UUlDSDRJTGxjME5PVWJPK2JSQ3dOTnZ2cVdOL3FRS3NmWFdXamd1K1JNRC0tTzM5Y09KZVhMZVM1aXZhNlFpUFJ0dz09--2c592fb3564672638b7e8c515577041d19ff4cd8; dtPC=2$503247007_880h3vPFAPDDCMSSTPCHTIBKAAAUUTMEQHRFCH-2e48; dtCookie=v_4_srv_36_sn_HGDM0E9GKCRC8CCD7LVKPELF6VR0D2AH_perc_100000_ol_0_mul_1_app-3Afff1ee41ce05f800_1_app-3A9a85821213a24845_1_app-3A1bc3b8a52b571c99_1_app-3Aac58787e2e32ae53_1_app-3A8bc7ac3ff70c4079_1; rxvt=1600705074840|1600701358805'
    }
    r = requests.post( url ,verify=ssl_verify, headers=headers )
    if ( r.status_code not in [200, 201, 204] ):
        msg = 'Error! code=' + str(r.status_code) + ', content=' + r.text
        err = True
    else:
        if ( r.status_code == 204 ):
            msg = 'OK ' + str(r.status_code)
        else:
            msg = r.text
        err = False
    return err, msg

## VALIDATE ##
def http_post_validate(url, token, data, ssl_verify=False):
    # response 204
    payload = json.dumps(data, indent=4)
    headers = {
        "accept" : "application/json",
        "charset" : "utf-8",
        "Authorization" : "Api-Token " + token ,
        'Content-Type': "application/json",
        'Cache-Control': "no-cache",
        'Accept-Encoding': "gzip, deflate",
        'Connection': "keep-alive",
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
        'Cookie' : '_gcl_au=1.1.672628857.1597240908; _ft_info=%7B%22utm_campaign%22%3A%22none%22%2C%22utm_content%22%3A%22none%22%2C%22utm_medium%22%3A%22website%22%2C%22utm_source%22%3A%22organic%22%2C%22utm_term%22%3A%22none%22%2C%22vehicle_name%22%3A%22none%22%2C%22landingpage%22%3A%22https%3A//www.dynatrace.com/news/category/product-news/%22%2C%22original_referrer%22%3A%22none%22%7D; prexisthb=%7B%22utm_campaign%22%3A%22none%22%2C%22utm_content%22%3A%22none%22%2C%22utm_medium%22%3A%22website%22%2C%22utm_source%22%3A%22organic%22%2C%22utm_term%22%3A%22none%22%2C%22vehicle_name%22%3A%22none%22%2C%22landingpage%22%3A%22https%3A//www.dynatrace.com/news/category/product-news/%22%2C%22original_referrer%22%3A%22none%22%7D; _ga=GA1.2.593057164.1597240915; _mkto_trk=id:352-NVO-562&token:_mch-dynatrace.com-1597240915260-75640; _fbp=fb.1.1597240915799.1453774814; p23mn32t=TH23TSF6DAH6JBQV525GCDE7OQ; _vwo_uuid_v2=D0EFA74BC8C40319699907DFAD2ADFF7F|a5ed6179c5987dbcc7b5bf20f4a962a7; _vis_opt_s=1%7C; _vwo_uuid=D0EFA74BC8C40319699907DFAD2ADFF7F; _vwo_ds=3%241598451425%3A29.14773939%3A%3A; _rxt_cookiepolicy=1; rxVisitor=1597240906752ACLSA5Q0NLKI25PQ9GU0RAS2CUFBF064; _gid=GA1.2.559498932.1600674009; rxsession==3=srv=4=sn=F9CA8486E793B8412DAE4CF019E57602=perc=100000=ol=0=mul=1=app:7fb64fd3b202c513=1=app:366f9fc79607e4b1=1; b925d32c=QX4I5CYD6B3I5CG2FL3OMHK5FE; ssoCSRFCookie=8d6c8371511e6fefd2079d10bb0f872333848efd862e37fe7ab9031de0d51f7e; JSESSIONID=E176177E8027AC86933F5866272B4653; apmsessionid=node01rxljisckl3jg1s53j73b7wjq6468.node0; dtSa=-; rxpc=4$502150672_195h-vKSCMKMDUFSTOHTVNMGDHJAEFCFUQKWUF-0e5; rxlatency=1; dtLatC=1; dtCookie=4$HGDM0E9GKCRC8CCD7LVKPELF6VR0D2AH|fff1ee41ce05f800|1|9a85821213a24845|1|1bc3b8a52b571c99|1|ac58787e2e32ae53|1|8bc7ac3ff70c4079|1; intercom-session-emeshyeu=V3JMSk9DSEtOejVRSGJWRklaQmh1UUlDSDRJTGxjME5PVWJPK2JSQ3dOTnZ2cVdOL3FRS3NmWFdXamd1K1JNRC0tTzM5Y09KZVhMZVM1aXZhNlFpUFJ0dz09--2c592fb3564672638b7e8c515577041d19ff4cd8; dtPC=2$503247007_880h3vPFAPDDCMSSTPCHTIBKAAAUUTMEQHRFCH-2e48; dtCookie=v_4_srv_36_sn_HGDM0E9GKCRC8CCD7LVKPELF6VR0D2AH_perc_100000_ol_0_mul_1_app-3Afff1ee41ce05f800_1_app-3A9a85821213a24845_1_app-3A1bc3b8a52b571c99_1_app-3Aac58787e2e32ae53_1_app-3A8bc7ac3ff70c4079_1; rxvt=1600705074840|1600701358805'
    }
    r = requests.post( url ,verify=ssl_verify, headers=headers, data=payload )
    if ( r.status_code != 204 ):
        msg = 'Error! code=' + str(r.status_code) + ', content=' + r.text
        err = True
    else:
        msg = 'OK ' + str(r.status_code) + '\n' + payload
        err = False
    return err, msg

## PUT ##
def http_put(url, token, data, ssl_verify=False):
    # response 201 (created)
    # response 204 (updated - no body in resp)
    # response 400 (failed)
    payload = json.dumps(data, indent=4)
    headers = {
        "accept" : "application/json",
        "charset" : "utf-8",
        "Authorization" : "Api-Token " + token ,
        'Content-Type': "application/json",
        'Cache-Control': "no-cache",
        'Accept-Encoding': "gzip, deflate",
        'Connection': "keep-alive",
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
        'Cookie' : '_gcl_au=1.1.672628857.1597240908; _ft_info=%7B%22utm_campaign%22%3A%22none%22%2C%22utm_content%22%3A%22none%22%2C%22utm_medium%22%3A%22website%22%2C%22utm_source%22%3A%22organic%22%2C%22utm_term%22%3A%22none%22%2C%22vehicle_name%22%3A%22none%22%2C%22landingpage%22%3A%22https%3A//www.dynatrace.com/news/category/product-news/%22%2C%22original_referrer%22%3A%22none%22%7D; prexisthb=%7B%22utm_campaign%22%3A%22none%22%2C%22utm_content%22%3A%22none%22%2C%22utm_medium%22%3A%22website%22%2C%22utm_source%22%3A%22organic%22%2C%22utm_term%22%3A%22none%22%2C%22vehicle_name%22%3A%22none%22%2C%22landingpage%22%3A%22https%3A//www.dynatrace.com/news/category/product-news/%22%2C%22original_referrer%22%3A%22none%22%7D; _ga=GA1.2.593057164.1597240915; _mkto_trk=id:352-NVO-562&token:_mch-dynatrace.com-1597240915260-75640; _fbp=fb.1.1597240915799.1453774814; p23mn32t=TH23TSF6DAH6JBQV525GCDE7OQ; _vwo_uuid_v2=D0EFA74BC8C40319699907DFAD2ADFF7F|a5ed6179c5987dbcc7b5bf20f4a962a7; _vis_opt_s=1%7C; _vwo_uuid=D0EFA74BC8C40319699907DFAD2ADFF7F; _vwo_ds=3%241598451425%3A29.14773939%3A%3A; _rxt_cookiepolicy=1; rxVisitor=1597240906752ACLSA5Q0NLKI25PQ9GU0RAS2CUFBF064; _gid=GA1.2.559498932.1600674009; rxsession==3=srv=4=sn=F9CA8486E793B8412DAE4CF019E57602=perc=100000=ol=0=mul=1=app:7fb64fd3b202c513=1=app:366f9fc79607e4b1=1; b925d32c=QX4I5CYD6B3I5CG2FL3OMHK5FE; ssoCSRFCookie=8d6c8371511e6fefd2079d10bb0f872333848efd862e37fe7ab9031de0d51f7e; JSESSIONID=E176177E8027AC86933F5866272B4653; apmsessionid=node01rxljisckl3jg1s53j73b7wjq6468.node0; dtSa=-; rxpc=4$502150672_195h-vKSCMKMDUFSTOHTVNMGDHJAEFCFUQKWUF-0e5; rxlatency=1; dtLatC=1; dtCookie=4$HGDM0E9GKCRC8CCD7LVKPELF6VR0D2AH|fff1ee41ce05f800|1|9a85821213a24845|1|1bc3b8a52b571c99|1|ac58787e2e32ae53|1|8bc7ac3ff70c4079|1; intercom-session-emeshyeu=V3JMSk9DSEtOejVRSGJWRklaQmh1UUlDSDRJTGxjME5PVWJPK2JSQ3dOTnZ2cVdOL3FRS3NmWFdXamd1K1JNRC0tTzM5Y09KZVhMZVM1aXZhNlFpUFJ0dz09--2c592fb3564672638b7e8c515577041d19ff4cd8; dtPC=2$503247007_880h3vPFAPDDCMSSTPCHTIBKAAAUUTMEQHRFCH-2e48; dtCookie=v_4_srv_36_sn_HGDM0E9GKCRC8CCD7LVKPELF6VR0D2AH_perc_100000_ol_0_mul_1_app-3Afff1ee41ce05f800_1_app-3A9a85821213a24845_1_app-3A1bc3b8a52b571c99_1_app-3Aac58787e2e32ae53_1_app-3A8bc7ac3ff70c4079_1; rxvt=1600705074840|1600701358805'
    }
    r = requests.put( url ,verify=ssl_verify, headers=headers, data=payload )
    if ( r.status_code not in [200, 201, 204] ):
        msg = 'Error! code=' + str(r.status_code) + ', content=' + r.text
        err = True
    else:
        if ( r.status_code == 204 ):
            msg = 'OK ' + str(r.status_code)
        else:
            msg = r.text
        err = False
    return err, msg

## DELETE ##
def http_delete(url, token, ssl_verify=False):
    # response 204
    headers = {
        "accept" : "application/json",
        "charset" : "utf-8",
        "Authorization" : "Api-Token " + token ,
        'Content-Type': "application/json",
        'Cache-Control': "no-cache",
        'Accept-Encoding': "gzip, deflate",
        'Connection': "keep-alive"
    }
    r = requests.delete( url ,verify=ssl_verify, headers=headers )
    if ( r.status_code not in [200, 204] ):
        msg = 'Error! code=' + str(r.status_code) + ', content=' + r.text + ', url=' + url
        err = True
    else:
        msg = 'Delete OK code=' + str(r.status_code) + ', url=' + url
        err = False
    return err, msg

## CHECK ##
def check_for_errors(error, message,debug=False):
    if not error:
        if debug:
            print(str(message))
    else:
        print(str(message))
        #sys.exit(1)
    return

def exit_with_msg(msg):
    print(str(msg))
    #sys.exit(1)
    return

def file_exists(file):
    r = os.path.exists(file)
    return r
