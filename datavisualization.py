from PIL import Image
import requests
from io import BytesIO
import zipfile
import pathlib 
import random
import os
from data_extraction import load_data

def visualize_data:
    try:
        url = load_data()
        url_response = requests.get(url)
        url_response.raise_for_status()  # Raise an error for bad responses
        with zipfile.ZipFile(BytesIO(url_response.content)) as z:
            z.extractall('.')
        print("Data extraction successful.")
    except requests.exceptions.RequestException as e:
        print("Error downloading data:", e)
    except zipfile.BadZipFile:
        print("The downloaded file is not a valid zip file.")
    except Exception as e:
        print("An unexpected error occurred:", e)

    normal_images = os.listdir(os.path.join(os.getcwd(),'tuberculosis_xray_data/Normal'))
    tuberculosis_images = os.listdir(os.path.join(os.getcwd(),'tuberculosis_xray_data/Tuberculosis'))
    path = pathlib.Path(os.path.join(os.getcwd(),'tuberculosis_xray_data'))

    def open_random_image(path):
        # Get a list of all files in the folder
        all_files = os.listdir(path)
        random_image_file = random.choice(all_files)
        image_path = os.path.join(path, random_image_file)
        image = Image.open(image_path)
        return image

    normal_image_1 = open_random_image(os.path.join(os.getcwd(),'tuberculosis_xray_data/Normal'))
    normal_image_1.save('normal_xray_01.jpg')
    normal_image_2 = open_random_image(os.path.join(os.getcwd(),'tuberculosis_xray_data/Normal'))
    normal_image_2.save('normal_xray_02.jpg')
    tuberculosis_image_1 = open_random_image(os.path.join(os.getcwd(),'tuberculosis_xray_data/Tuberculosis'))
    tuberculosis_image_1.save('tuberculosis_xray_01.jpg')
    tuberculosis_image_2 = open_random_image(os.path.join(os.getcwd(),'tuberculosis_xray_data/Tuberculosis'))
    tuberculosis_image_2.save('tuberculosis_xray_02.jpg')

    return path, normal_images, tuberculosis_images

visualize_data()
