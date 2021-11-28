


To source for the packages from gitrepo:

import json
import sys
import requests
import github3
from github import Github
from lxml import etree
import xml.etree.ElementTree as ET
parser = etree.XMLParser(recover=True)
access_token = str(sys.argv[2])
username = str(sys.argv[1])
orgName = str(sys.argv[3])
g=github3.github.GitHubEnterprise(url='https://github.88-internal.com', token=access_token) # You will need to enter your access token from github enterprise

result = []
packageinfo = ()
org = g.organization(orgName)
repos = list(org.repositories())


def PackagesConfig(packagelist):

    for abelnow in repos:

        var = "packages.config in:path repo:" + str(abelnow)
        result = g.search_code(var)
     
        for file in result:
            url = file.html_url.replace("https://github.88-internal.com", "https://github.88-internal.com/raw").replace("blob/", "") 
            r = requests.get(url, auth=(username, access_token))
            xmldata =r.content.decode("utf-8")
            for line in xmldata.splitlines():

                rec = line.strip()                            
    
                if rec.startswith("<package id="):
                    xml_string = rec.replace("/>","></package>") 
                    root = ET.fromstring(xml_string)
                    
                    packageinfo=(root.attrib['id'], root.attrib['version']) 
                    
                    
                    if packageinfo not in packagelist:                        
                        packagelist.append(packageinfo)


def csprojPackages(packagelist):
    for abelnow in repos:

        var = "csproj in:path repo:" + str(abelnow)
        result = g.search_code(var)
     
        for file in result:
            url = file.html_url.replace("https://github.88-internal.com", "https://github.88-internal.com/raw").replace("blob/", "") # 
            r = requests.get(url, auth=(username, access_token))
            xmldata =r.content.decode("utf-8")
            
            for line in xmldata.splitlines():
                rec = line.strip()
                
                if rec.startswith("<PackageReference"):
                    xml_string = rec.replace("/>","></PackageReference>").replace(">","></PackageReference>")
                    root = ET.fromstring(xml_string, parser=parser)
                    if 'Include' in root.attrib:
                        if 'Version' in root.attrib:
                            packageinfo = (root.attrib['Include'], root.attrib['Version'])

                            if packageinfo not in packagelist:
                                packagelist.append(packageinfo)

                


packageL = {} 
PackagesConfig(packageL)
csprojPackages(packageL)


To package result into json
jsonlist = json.dumps(packageL, indent=3)
#print(jsonlist)
open("packagelist.json", "w" ).write(jsonlist)
