# -*- coding: utf-8 -*-
"""
Created on Mon May 24 10:38:32 2021

@author: clair
"""

import xml.etree.ElementTree as ET
import pandas as pd 
import requests as re  

#將網站上的emic資料複製下來存到自己的電腦上
url="https://portal2.emic.gov.tw/Pub/DIM2/OpenData/Disaster.xml"
resp = re.get(url, headers = {
        "user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36" 
    })
resp.encoding = 'utf-8-sig'
f = open('emic2.0.xml' , 'w' , encoding = 'utf-8-sig')
f.write(resp.text)

#將需要的資料轉成csv檔
xmlparse = ET.parse('emic.xml')
root = xmlparse.getroot()
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
    DISASTER_MAIN_TYPE = "None" if DISASTER_MAIN_TYPE_NODE is None  else DISASTER_MAIN_TYPE_NODE.text
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

