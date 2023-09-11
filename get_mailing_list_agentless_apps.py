import json
import requests
import os
import urllib3

##################################
### Environment managed
##################################

#Cluster=os.getenv('Cluster')
ClusterToken=os.getenv('ClusterToken')

##################################
## Variables
##################################
Mapping = {}
API_GET_USERS="/api/v1.0/onpremise/users"
USER_GROUPS = "/api/v1.0/onpremise/groups"

#DEV
ENV='DEV'
#agentless
sias = ["1po","adt","dfw","dog","dpt",'du5',"gfe","ols","mch","mvr","pne","pu5","rbo","sp2","spx","tot","ttt","uca","ps2"]
#mobile
#sias = ["myr","mom","mym","poc","egw","skf","rtm","mpc","gli","pss","spx","rsk","nmd"]

#RE7
#ENV='RE7'
#agentless
#sias = ["adt","dfw","dog","dpt","mvr","mch","p7b","pne","rac","rbo","npd","ols","sp2","ttt","uca"]
#mobile
#sias = ["mym","egw","nmd","mpc","myr","mom","skf","spx","rsk"]

#OPE
#ENV='OPE'
#agentless
#sias = ["hb2","snt","ezf","mob","nfs","dog","mpo","rds","ttt","dr9","dfw","dpt","wbo","pvd","lov","pne","wrd","dog","gmk","ols","rbo","dfm","spx","rac","ccb","wbo","mch","ikr","rnm","sfa","grp","rsk","csb","p7b","hri","sp2","pwo","snw","pli","trb","mvr","tag","wd3"]
#mobile
#sias = ["rsk","egw","skf","spx","mpc","mym","myr","nmd","mom","gli","rbo"]

# variable changed if script is run on Windows or Linux. "\\" for Windows, "/" for Linux
DIRECTORY = "./mailing_list/"
if os.name == 'nt':
    DIRECTORY = ".\\mailing_list\\"

#disable warning
urllib3.disable_warnings()
RESULT={}

#TODO modify Cluster url, X-CSRFToken and Cookie:
Cluster = 'https://fca8afff-feb2-44e0-871d-ca4c9ab9f307-50.managed.internal.dynatrace.com:8021'
ClusterToken = ''
head = {
    'Accept': 'application/json',
    'Content-Type': 'application/json; charset=UTF-8',
    'Authorization': 'Api-Token {}'.format(ClusterToken),
    'X-CSRFToken': 'c30be076-76e2-4f40-96ba-18fd8e738490|50|fca8afff-feb2-44e0-871d-ca4c9ab9f307',
    'Cookie': 'p23mn32t=227GOKIKZN6NWJZWOHIH2QIUS4; _mkto_trk=id:352-NVO-562&token:_mch-dynatrace.com-1661176622950-84496; _fbp=fb.1.1664263895588.1802444479; _hjSessionUser_2803510=eyJpZCI6ImU2MjlmNjkzLTYyMzMtNTQ5My1iN2RlLWZmN2U5NDAwMGM4NyIsImNyZWF0ZWQiOjE2NjIwMjE1NjgyNjksImV4aXN0aW5nIjp0cnVlfQ==; ajs_anonymous_id=7a8f6026-05b5-48b6-871d-2c009214427c; OptanonAlertBoxClosed=2023-04-27T07:08:46.355Z; _gcl_au=1.1.811854470.1692695565; rxVisitor=16922730016691MOP04B9NF4JNVK50CKG8J5QCRBF1EO8; artemis-recent-searches=W10=; visitorId=IjNlNDA0MTZjLWJhYTYtNDhhZC1hZjlmLWY3OTYwNDc2ZjE0NCI=; _ft_info=%7B%22utm_campaign%22%3A%22none%22%2C%22utm_content%22%3A%22none%22%2C%22utm_medium%22%3A%22website%22%2C%22utm_source%22%3A%22organic%22%2C%22utm_term%22%3A%22none%22%2C%22vehicle_name%22%3A%22none%22%2C%22landingpage%22%3A%22https%3A//www.dynatrace.com/news/blog/slo-monitoring-alerting-on-slos-error-budget-burn-rates/%22%2C%22original_referrer%22%3A%22none%22%7D; coveo_visitorId=acccb944-591f-4100-9ec8-7394bf331606; prexisthb=%7B%22utm_campaign%22%3A%22fr-brand%22%2C%22utm_content%22%3A%22EAIaIQobChMIq-fX4ZGbgQMVL4BQBh1AlAh7EAAYASABEgLGsvD_BwE%22%2C%22utm_medium%22%3A%22cpc%22%2C%22utm_source%22%3A%22google%22%2C%22utm_term%22%3A%22dynatrace%22%2C%22vehicle_name%22%3A%22none%22%2C%22landingpage%22%3A%22https%3A//www.dynatrace.com/hub/%22%2C%22original_referrer%22%3A%22https%3A//www.google.com/%22%7D; _gcl_aw=GCL.1694180392.EAIaIQobChMIq-fX4ZGbgQMVL4BQBh1AlAh7EAAYASABEgLGsvD_BwE; _gcl_dc=GCL.1694180392.EAIaIQobChMIq-fX4ZGbgQMVL4BQBh1AlAh7EAAYASABEgLGsvD_BwE; _gac_UA-54510554-1=1.1694180394.EAIaIQobChMIq-fX4ZGbgQMVL4BQBh1AlAh7EAAYASABEgLGsvD_BwE; ABTasty=uid=3pz5tsmw4phvvy51&fst=1694075763755&pst=1694079866855&cst=1694180392749&ns=3&pvt=8&pvis=6&th=; BE_CLA3=p_id%3D6P6N6NRPP624R8LNN2RNN4P8AAAAAAAAH%26bf%3D96327fdab26c0fde654068955b129e60%26bn%3D1%26bv%3D3.46%26s_expire%3D1694502649419%26s_id%3DNP6N6NRPP624R6L2JN6RNN4P8AAAAAAAAH; OptanonConsent=isGpcEnabled=0&datestamp=Mon+Sep+11+2023+09%3A10%3A51+GMT%2B0200+(Central+European+Summer+Time)&version=202305.1.0&isIABGlobal=false&hosts=&consentId=9c66e78b-a66b-4ba3-983e-535b608d0b88&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1&browserGpcFlag=0&geolocation=FR%3BIDF&AwaitingReconsent=false; _uetsid=57878580507211ee8d119d0669ed6887; _uetvid=c4a657d08a8911ec9a0189792e626a96; _gid=GA1.2.1938238195.1694416254; _ga=GA1.1.854216105.1661176622; _ga_1MEMV02JXV=GS1.1.1694421440.59.1.1694423745.0.0.0; b925d32c=FCCVSDNUYQWRTCJ7BTTH3VCW6I; ssoCSRFCookie=931b3b942d9d06aa0c653fc048c3e537df94afe825834861ba4013a9b73bef47; JSESSIONID=node015z81zw2edx22qgo1io3iz8je4919.node0; dtCookie=v_4_srv_12_sn_C26E825D4C27A7241B49458D846D8E74_perc_100000_ol_0_mul_1_app-3A8b7f8c9bf559d84c_1_app-3Af6b10dd0df01cfe1_1_app-3A98ef57ca1ba5392b_1_app-3Af11087ed2451f443_1_app-3A7fb64fd3b202c513_1_app-3Aea7c4b59f27d43eb_1_app-3A9a85821213a24845_1_app-3Abb68032936bb9776_1_app-3Aeb632aef1827f23b_1_app-3A50afbf2023ba0be6_1_app-3A0f516f0fa5413c27_1_rcs-3Acss_0; apmsessionid=node01myo9b8x1580i107uo835963ca282841.node0; dtSa=-; rxvt=1694430449428|1694413652850; dtPC=12$28619290_498h-vQCWKNCDPEUFFVHVFWEHMGWNKPLVFEMFD-0e0'	
}



##################################
## Generic Dynatrace API
##################################

# generic function GET to call API with a given uri
def queryDynatraceAPI(uri):
    jsonContent = None
    response = requests.get(uri,headers=head,verify=False)
    # For successful API call, response code will be 200 (OK)
    if(response.ok):
        if(len(response.text) > 0):
            jsonContent = json.loads(response.text)
    else:
        jsonContent = json.loads(response.text)
        #print(jsonContent)
        errorMessage = ""
        if(jsonContent["error"]):
            errorMessage = jsonContent["error"]["message"]
            print("Dynatrace API returned an error: " + errorMessage)
        jsonContent = None
        #raise Exception("Error", "Dynatrace API returned an error: " + errorMessage)

    return(jsonContent)


   
##################################
## list of API
##################################
def info_api(TENANT,TOKEN,API):
    #uri=TENANT+API+'?Api-Token='+TOKEN
    uri=TENANT+API
    RESULT={}

    print(uri+'?Api-Token='+TOKEN)
    listentityid=[]
    DoublonTodelete=[]
    datastore = queryDynatraceAPI(uri)
    print(datastore)
    if datastore != []:
        for apilist in datastore :
            #print(apilist)
            RESULT[apilist['email']]=apilist['groups']
        
    return (RESULT)

##################################
## Main program
##################################
if not(os.path.exists(DIRECTORY)):
    os.makedirs(DIRECTORY)

RESULT=info_api(Cluster, ClusterToken, API_GET_USERS)
fichier = open(DIRECTORY+ENV+'-sia_email_mapping.csv', "w")
i=0
for sia in sias:
    print(sia)
    fichier.write(sia+"\n")
    for user in RESULT:
        if sia in RESULT[user]:
            #print(user)
            print(user , end=";")
            fichier.write(user+";")
            i+=1
    fichier.write("\n")
fichier.close()
print(i)
print("end")


    

