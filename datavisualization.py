import os
import plotly.express as px
import numpy as np
from PIL import Image
from data_extraction import load_data

def preprocess_image(image_path, target_size=(256, 256)):
    img = Image.open(image_path).convert('L')
    img.thumbnail(target_size)  # Preserve aspect ratio
    img_array = np.array(img)
    # Pad the image to ensure the target size (optional)
    padded_array = np.pad(img_array, [(0, target_size[1] - img_array.shape[0]), 
                                     (0, target_size[0] - img_array.shape[1])], mode='constant', constant_values=0)
    return padded_array

def get_file_name(file_path):
    return os.path.basename(file_path)

def visualize_data():
    data = load_data()

    # Get value counts of the labels
    label_counts = data['label'].value_counts().reset_index()
    label_counts.columns = ['X-Ray Type', 'Number of Cases']
    label_counts['X-Ray Type'] = label_counts['X-Ray Type'].replace({0: 'Normal', 1: 'Tuberculosis'})

    # Create a bar graph
    fig_1 = px.bar(label_counts, x='X-Ray Type', y='Number of Cases', title='Distribution of X-Ray Cases')
    fig_1.update_xaxes(showgrid=False)
    fig_1.update_yaxes(showgrid=False)
    fig_1.show()
    fig_1.write_image('fig_1.jpg')

    # Get a few samples for both classes
    Tuberculosis_samples = data[data['label'] == 1]['image_path'].iloc[:5].tolist()
    normal_samples = data[data['label'] == 0]['image_path'].iloc[:5].tolist()

    # Concatenate the data in a single list
    samples = normal_samples + Tuberculosis_samples
    print(samples)
    sample_labels = [f'Tuberculosis:<br>{get_file_name(path)}' for path in Tuberculosis_samples] + \
                    [f'Normal:<br>{get_file_name(path)}' for path in normal_samples]

    # Preprocess images and stack into a single NumPy array
    images = np.array([preprocess_image(img_path) for img_path in samples])

    # Use px.imshow to display images
    fig_2 = px.imshow(images, facet_col=0, facet_col_wrap=5, binary_string=True, labels={'facet_col': 'X-Ray Type'})
    
    # Update facet titles to include image file names
    for i, annotation in enumerate(fig_2.layout.annotations):
        annotation.text = sample_labels[i]

    fig_2.update_layout(height=600, width=1000, title_text="Sample X-Ray Images")
    fig_2.show()
    fig_2.write_image('fig_2.jpg')

    data.to_csv('tb_dataset.csv', index=False)

    return data

visualize_data()
