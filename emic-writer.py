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
  download_blob(event['bucket'], event['name'], '/tmp/'+event['name'])

  ids = open('/tmp/'+event['name']).read()
  for nid in ids:
    filename = f"{nid}.csv"
    _emic_csv_writer("/tmp/"+filename)
    upload_blob("emic-csv-cla", "/tmp/"+filename, filename)

#將該檔案解析後儲存為csv檔
def _emic_csv_writer(filename):
  xmlparse = ET.parse( filename )
  root = xmlparse.getroot()
  rows = []
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
  df.to_csv( filename , encoding = 'utf-8')
