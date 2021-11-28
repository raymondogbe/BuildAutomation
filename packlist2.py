This python script calls each of the nuget package and version from the json file in the git repo.
This script is run automatically in a jenkins job, which triggers another jenkins job (jenkins_url)

import requests,json

#jenkins_url="https://sccjenkins1.corp.88-internal.com/job/DDS_Sigining_Test_Pipe/buildWithParameters"
jenkins_url="https://sccjenkins1.corp.88-internal.com/job/DDS_Sigining_Test_Prod_Install/buildWithParameters"

auth=("username","token")

with open('Successfu_packages.json') as f:
    data = json.load(f)
    for package in data['Packages']:
        NUGET_PAK = (package['package_name'])
        NUGET_Ver = (package['package_ver'])
        jenkins_params={
            'NUGET_PAK': NUGET_PAK,
            'NUGET_Ver': NUGET_Ver 
        }

        print(jenkins_params)

        print(jenkins_url)

        response = requests.post(
            jenkins_url,auth=auth
            ,params=jenkins_params)

        print(response.status_code)
