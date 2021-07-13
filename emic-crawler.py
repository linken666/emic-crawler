import requests
import time

from google.cloud import storage

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
 
#cloud function啟動後將網頁複製下來並以不同的時間為檔名儲存在值區emic-crawler-cla
def main(request):  
  end = int(time.time())
  start = end - 3600

  url = f"https://portal2.emic.gov.tw/Pub/DIM2/OpenData/Disaster.xml"
  print(url)
  res = requests.get(url)
  res.encoding = 'utf-8'
  
  filename = f"emic_text_{int(time.time())}.xml"
  with open(f"/tmp/"+filename, "w", encoding = 'utf-8') as f:
    f.write(res.text)
  
  upload_blob("emic-crawler-cla", "/tmp/"+filename, filename)
