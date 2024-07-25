import os
from PIL import Image
import pandas as pd
import numpy as np

def load_data():
    normal_dir = 'Normal'
    tb_dir = 'Tuberculosis'
    
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

# data = load_data()
