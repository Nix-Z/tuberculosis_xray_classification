import os
import boto3
import requests
from io import BytesIO
import zipfile
from PIL import Image
import pandas as pd
import numpy as np

def load_data():
    s3 = boto3.client('s3')
    bucket_name = 'usecases-data'
    url = s3.generate_presigned_url(
                    ClientMethod='get_object',
                    Params={'Bucket': bucket_name, 'Key': 'tuberculosis_xray_data.zip'},
                    ExpiresIn=7200  # URL expiration time in seconds (adjust as needed)
                )
    print(url)
    url_response = requests.get(url)
    with zipfile.ZipFile(BytesIO(url_response.content)) as z:
        z.extractall('.')
    
    normal_dir = 'tuberculosis_xray_data/Normal'
    tb_dir = 'tuberculosis_xray_data/Tuberculosis'
    
    normal_files = [os.path.join(normal_dir, f) for f in os.listdir(normal_dir) if os.path.isfile(os.path.join(normal_dir, f))]
    tb_files = [os.path.join(tb_dir, f) for f in os.listdir(tb_dir) if os.path.isfile(os.path.join(tb_dir, f))]
    
    data = []
    
    for f in normal_files:
        data.append((f, 0))
    
    for f in tb_files:
        data.append((f, 1))
    
    data = pd.DataFrame(data, columns=['image_path', 'label'])

    data = data.sample(frac=1).reset_index(drop=True)

    print(data.head())
    
    return data

data = load_data()
