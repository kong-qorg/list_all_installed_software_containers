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
        result.append((item['imageId'], item['sha'], item['name']))
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





# def print_containers_details(container_list_data, token, podname):

#     containers_software_table = []
#     software_dict = {}
#     for item in container_list_data:
#         list_of_softwares = get_installed_softwares(str(item[1]), token, podname)
#         #print(f"\n\n\n\n ------- container Sha: {item[1]}, container name: {item[2]} --------")
#         #print(list_of_softwares)
        
#         # get the list of softwares installed in a specific container sha by calling 'parse_softwares' function
#         software_list = parse_softwares(json.dumps(list_of_softwares))

#         # adding the software list to the dictionary
#         software_dict['Container Id'] = item[0]
#         software_dict['Container Name'] = item[2]
#         software_dict['Software Lists'] = software_list
        
#         containers_software_table.append(software_dict)

#     # Finally print the list of all softwares
#     print("\n----- List of Software Installed --------\n")   
#     return containers_software_table




def print_containers_details(container_list_data, token, podname):

    uniq_container_list_data = list(set(container_list_data))
    software_dict = {}
    with open('output.csv','a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for item in uniq_container_list_data:
            list_of_softwares = get_installed_softwares(str(item[1]), token, podname)
            #print(f"\n\n\n\n ------- container Sha: {item[1]}, container name: {item[2]} --------")
            #print(list_of_softwares)
        
            # get the list of softwares installed in a specific container sha by calling 'parse_softwares' function
            software_list = parse_softwares(json.dumps(list_of_softwares))

            writer.writerow([item[0], item[2], software_list])
            # adding the software list to the dictionary
            #software_dict['Container Id'] = item[0]
            #software_dict['Container Name'] = item[2]
            #software_dict['Software Lists'] = software_list
        
            #containers_software_table.append(software_dict)

    csvfile.close()
    # Finally print the list of all softwares
    
    
    with open('output.csv','r') as file:
        reader = csv.reader(file)
        rows = [row for row in reader]

    unique_rows = []

    for row in rows:
        if row not in unique_rows:
            unique_rows.append(row)


    with open('output.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(unique_rows)

