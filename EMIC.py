# -*- coding: utf-8 -*-
"""
Created on Mon May 24 10:38:32 2021

@author: clair
"""

import xml.etree.ElementTree as ET
import pandas as pd 

xmlparse = ET.parse('emic.xml')
root = xmlparse.getroot()

cols = ["CASE_ID", "CASE_DT", "CASE_LOC", "DISASTER_MAIN_TYPE", "CASE_DESCRIPTION"]
rows = []

print(root[1].tag)

cnt = 0

for i in root[1].findall('{http://emic.eoc.gov.tw/disaster_info}DISASTER_DATA'):
    print(cnt)
    cnt += 1
    CASE_ID = i.find("{http://emic.eoc.gov.tw/disaster_info}CASE_ID").text
    CASE_DT = i.find("{http://emic.eoc.gov.tw/disaster_info}CASE_DT").text
    CASE_LOC = i.find("{http://emic.eoc.gov.tw/disaster_info}CASE_LOC").text
    DISASTER_MAIN_TYPE_NODE = i.find("{http://emic.eoc.gov.tw/disaster_info}DISASTER_MAIN_TYPE")
    DISASTER_MAIN_TYPE = "QQ" if DISASTER_MAIN_TYPE_NODE is None  else DISASTER_MAIN_TYPE_NODE.text
    CASE_DESCRIPTION = i.find("{http://emic.eoc.gov.tw/disaster_info}CASE_DESCRIPTION").text
    print(CASE_ID)
    
    rows.append({"CASE_ID": CASE_ID,
                 "CASE_DT": CASE_DT,
                 "CASE_LOC": CASE_LOC,
                 "DISASTER_MAIN_TYPE": DISASTER_MAIN_TYPE,
                 "CASE_DESCRIPTION": CASE_DESCRIPTION
                 })
    
df = pd.DataFrame(rows)
df.to_csv('output.csv' , encoding = 'utf-8-sig')

import csv
#python2可以用file替代open
with open("test.csv","w") as csvfile: 
 writer = csv.writer( csvfile )
 writer.writerows( rows )
