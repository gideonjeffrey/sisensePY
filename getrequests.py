import sisenseconfig as config
import requests


def get_auth():
    """
    Returns the authentication token needed to access other REST API endpoints.
    """
    url = config.base_url + "/api/v1/authentication/login"

    payload = {
        "username": config.sisense_credentials["username"],
        "password": config.sisense_credentials["password"]
        }

    headers = {
        "content-type": "application/x-www-form-urlencoded"
        }

    auth_response = requests.request("POST", url, data=payload, headers=headers)
    try:
        auth_token = "Bearer " + auth_response.json()["access_token"]
        return(auth_token)
    except KeyError:
        print("Authentication failed; request status code = " + str(auth_response.status_code))
        print("Please verify the accuracy of the information stored in sisenseconfig.py.")
        return False


def get_elasticubes():
    """
    Returns every standard elasticube the user has access to BUT NOT live models.
    """
    token = get_auth()
    
    if token:
        url = config.base_url + "/api/v1/elasticubes/getElasticubes"
        headers = {
            'Accept': 'application/json',
            'Authorization': token
            }
        cube_response = requests.request("GET", url, headers=headers)
        if cube_response.status_code == 200:
            return cube_response.json()
        else:
            print("Status code " + str(cube_response.status_code) + "; cubes not fetched.")
            return []
    else:
        return []
