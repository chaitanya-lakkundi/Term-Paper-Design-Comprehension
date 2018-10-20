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
import simpleflock
from os.path import exists

for project_name, xmi_link in all_xmis:
    filename = "scraped_xmis/" + project_name.replace("/", "_") + xmi_link.split("/")[-1]
    
    with simpleflock.SimpleFlock("/tmp/scrape_select_file"):
        if exists(filename):
            continue
        else:
            open(filename, "w").close()

    print(xmi_link)
    page = requests.get(xmi_link)

    with simpleflock.SimpleFlock("/tmp/scrape_file_write"):
        with open(filename, "wb") as f:
            f.write(page.content)
