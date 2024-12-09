from auth import get_jwt_token, getListOfContainers, parse_json, print_containers_details
from csv_module import convert_to_csv
import os
import json

def main():
    username='user1'
    password='pass123'
    #username = os.getenv('username')
    #password = os.getenv('password')
    podname = 'https://gateway.qg2.apps.qualys.com'

    #### Get Token ###
    token = get_jwt_token(username, password, podname)

    

    #### Get the JSON Data body ####
    list_of_containers = getListOfContainers(token, podname)


    #### Get a list of containers and respective softwares installed on it ####
    
    image_list = parse_json(json.dumps(list_of_containers))

    print_containers_details(image_list, token, podname)

    print('######### Done with writing the Software list to outputs.csv file, please check your local directory #########')

if __name__ == '__main__':
    main()
