import sisenseconfig as config
import requests
import os


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


def get_smodel(cube_name, target_directory, oid=None):
    pass


def get_smodels(target_directory):
    pass


def dash_export():
    pass


def get_dashboards(fields="all", dashboard_type="owner", datasource="all"):
    """
    Returns an array of dashboards, using the /api/v1/dashboards/admin endpoint.

    For full information on this endpoint, see the documentation at 

    **The dashboard_type argument**

    Running get_dashboards() with no arguments returns complete JSON for every dashboard on the server where dashboard_type = "owner".
    Do this if you want **one unique record for every dashboard OID**, ignoring shared / proxy instances of the dashboard.

    Running get_dashboards(dashboard_type="all"), by contrast, returns ALL dashboards:
    every combination of dashboard / viewer (OID / userID) will be returned, since each dashboard share is its own dashboard object.

    Other valid inputs for dashboard_type are "user" and "proxy".

    **The datasource argument**

    You can set the datasource argument to the name of a particular model, e.g. "My Favorite Elasticube," if you only want to return
    dashboards that have that model as their datasource.

    **The 

    Dashboard objects are large!  If you want to restrict the amount of data returned, you can do one of the following:

    (1) Set fields to "summary" - returns only title, desc, shares, instanceType, oid, userId, created, lastUpdated, script, lastOpened, datasource,
    and viewerCount for each dashboard.

    (2) Set fields to a string of comma-separated fields you want returned, e.g. "title,oid,userId".
    
    """

    token = get_auth()

    if token:
        url = config.base_url + "/api/v1/dashboards/admin"
        
        headers = {
            'Accept': 'application/json',
            'Authorization': token
            }

        payload = {}

        #Populate payload fields attribute
        if fields == "all":
            pass
        elif fields == "summary":
            payload["fields"] = "title,desc,shares,instanceType,oid,userId,created,lastUpdated,script,lastOpened,datasource,viewerCount"
        else:
            payload["fields"] = fields

        if dashboard_type == "all":
            pass
        elif dashboard_type in ("owner", "user", "proxy"):
            payload["dashboardType"] = dashboard_type
        else:
            print('Error: must choose one of "all", "owner", "user", or "proxy" as dashboard-type.')
            raise ValueError

        if datasource == "all":
            pass
        else:
            payload["datasourceTitle"] = datasource
        
        #Get dashboards
        dash_response = requests.request("GET", url, params=payload, headers=headers)

        #Exception handling
        if dash_response.status_code == 200:
            return dash_response.json()
        else:
            print("Status code " + str(dash_response.status_code) + "; dashboards not fetched.")
            return []
    else:
        return []

def get_dashboard_scripts_file(filename, filepath, datasource="all"):
    """
    Returns a .txt file to the specified filepath containing title, OID, and script for every dashboard with an edited dashboard script.
    NOTE: adding a newline counts as an edit, so some scripts returned may not contain actual code.

    If you are interested in only scripts from dashboards built on one model/ElastiCube, enter "datasource='NAME_OF_MODEL'" as the third argument.
    """
    if datasource == "all":
        scripts_json = get_dashboards(fields="title,oid,script", dashboard_type="owner")
    else:
        scripts_json = get_dashboards(fields="title,oid,script", dashboard_type="owner", datasource=datasource)

    if scripts_json == []:
        print("No output file produced; no dashboard scripts found using these parameters.")
        return []
    
    os.chdir(filepath)
    if filename[-4:] == ".txt":
        with open(filename, 'w') as f:
            for dash in scripts_json:
                if "script" in dash:
                    f.write("Title: " + dash["title"] + "\n" + "OID: " + dash["oid"] + "\n\n" + dash["script"] + "\n\n\n\n******\n\n\n")
                else:
                    pass
    else:
        raise ValueError("Expected valid filename; please specify filename ending in '.txt'.")
    print(filename + " successfully created in " + filepath)
    return True


