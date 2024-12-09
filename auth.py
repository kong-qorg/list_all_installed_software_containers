import requests
import json, csv




def get_jwt_token(username, password, podname):

    #url = "https://gateway.qg2.apps.qualys.com/auth"
    url = f'{podname}/auth'
    payload = {'username': username, 'password': password, 'token': 'true'}
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.post(url, data=payload, headers=headers)
    token = response.text
    return token




def getListOfContainers(token, podname):
    
    url = f'{podname}/csapi/v1.3/containers?filter=state%3A%27RUNNING%27&pageNumber=1&pageSize=50&sort=created%3Adesc'
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()




def parse_json(json_data):

    result = []
    data = json.loads(json_data)
    for item in data['data']:
        result.append((item['imageId'], item['sha'], item['name'], item['containerId']))
    return result




def parse_softwares(json_data):

    result = []
    data = json.loads(json_data)
    for item in data['data']:
        result.append((item['name'], item['version']))
    return result



### Get a list of installed softwares for the specific Container Sha ###
def get_installed_softwares(container_sha, token, podname):

    url = f'{podname}/csapi/v1.3/containers/{container_sha}/software?isDrift=false'
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()  





def print_containers_details(container_list_data, token, podname):

    uniq_container_list_data = list(set(container_list_data))
    software_dict = {}
    with open('output.csv','a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for item in uniq_container_list_data:

            list_of_softwares = get_installed_softwares(str(item[1]), token, podname)

        
            # get the list of softwares installed in a specific container sha by calling 'parse_softwares' function
            software_list = parse_softwares(json.dumps(list_of_softwares))


            # print('\n ############ Writing ########',item[3], item[2], software_list)
            #software_dict['Container Id'] = item[3]
            #software_dict['Container Name'] = item[2]
            #software_dict['Software Lists'] = software_list            
            writer.writerow([item[3], item[2], software_list])

    # Finally Close the file
    csvfile.close()


