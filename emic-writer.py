import xml.etree.ElementTree as ET
import pandas as pd 

from google.cloud import storage


def download_blob(bucket_name, source_blob_name, destination_file_name):
    """Downloads a blob from the bucket."""
    # bucket_name = "your-bucket-name"
    # source_blob_name = "storage-object-name"
    # destination_file_name = "local/path/to/file"

    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)

    print(
        "Blob {} downloaded to {}.".format(
            source_blob_name, destination_file_name
        )
    )

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    # bucket_name = "your-bucket-name"
    # source_file_name = "local/path/to/file"
    # destination_blob_name = "storage-object-name"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(
        "File {} uploaded to {}.".format(
            source_file_name, destination_blob_name
        )
    )

#開啟先前上傳的檔案
def main(event, context):
  download_blob(event['bucket'], event['name'], '/tmp/'+event['name'])  #下載新增的xml檔
  filename = f"{event['name']}.csv"  #開一個csv
  pat = '/tmp/'+event['name']  #xml檔的路徑
  _emic_csv_writer(pat , filename)  #回傳給我csv
  upload_blob("emic-csv-cla", "/tmp/"+filename, filename)  #上傳到值區

#將該檔案解析後儲存為csv檔
def _emic_csv_writer(pat , filename):
  xmlparse = ET.parse( pat )  #解析路徑的xml
  root = xmlparse.getroot()  
  rows = []
  cnt = 0
#以下開始解析(這段之前在電腦上可以用)
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
    
  df = pd.DataFrame(rows)  #把rows做成DataFrame(像excel的那種表格)
  df.to_csv( filename , encoding = 'utf-8')  #把df輸出成csv檔
