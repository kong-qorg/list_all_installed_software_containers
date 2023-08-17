from auth import get_jwt_token, getListOfContainers, parse_json, print_containers_details
from csv_module import convert_to_csv
import os
import json

def main():
    username='username_goes_here'
    password='password_goes_here'
    #username = os.getenv('username')
    #password = os.getenv('password')
    podname = 'https://gateway.qg2.apps.qualys.com'

    #### Get Token ###
    token = get_jwt_token(username, password, podname)
    print(token)
    

    #### Get the JSON Data body ####
    list_of_containers = getListOfContainers(token, podname)
    print('********** Print list of Contianers ************')
    print(list_of_containers)

    #### Get a list of containers and respective softwares installed on it ####
    
    image_list = parse_json(json.dumps(list_of_containers))
    #print(image_list)
    container_software_table = print_containers_details(image_list, token, podname)
    print(container_software_table)

    # convert_to_csv(container_software_table)

if __name__ == '__main__':
    main()
