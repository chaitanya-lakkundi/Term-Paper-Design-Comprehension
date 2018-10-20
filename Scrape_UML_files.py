#!/usr/bin/env python
# coding: utf-8

# Chaitanya S Lakkundi

import csv
csvfile = open("UMLFiles_List_V2.0.csv")
data = csv.reader(csvfile)

all_xmis = []
for (name, link) in data:
    if link[-3:] == "xmi":
        all_xmis.append((name, link.replace("tree/master", "raw/master")))

import requests
import glob
scraped_xmis = glob.glob1("scraped_xmis", "*.xmi")

for project_name, xmi_link in all_xmis:    
    filename = project_name.replace("/", "_") + xmi_link.split("/")[-1]    
    if filename in scraped_xmis:
        continue
    print(xmi_link)
    page = requests.get(xmi_link)
    with open("scraped_xmis/"+filename, "wb") as f:
        f.write(page.content)
