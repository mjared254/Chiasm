import os
import yaml
import pandas as pd
from PIL import Image

FILE_PATH = '/Users/jaredmorales04/Chiasm/dataset_train_rgb/dataset_train_rgb'

if not os.path.exists(FILE_PATH):
    raise FileNotFoundError(f"Incorrect FilePath: {FILE_PATH}")
print(f"Dataset was found at {FILE_PATH}")


class BOSCHDataset():
    def __init__(self, yaml_path, files):
        self.yaml_path = yaml_path
        self.samples = []


        print(f"Loading data from YAML File {files}")
        #gets the yaml file name from the object we created and calls function to load and extract data from file
        for file_name in files:
            self.load_yaml_file(file_name)


        print(f"\n Total landed: {len(self.samples)} images with annotations")

        if len(self.samples) == 0:
            raise ValueError("No Images were loaded, check Dataset Structure")

    #loads and extracts the data from the yaml file.
    def load_yaml_file(self, file_name):
        train_file_path = os.path.join(FILE_PATH, file_name)

        if not os.path.exists(train_file_path):
            print(f"Annoations directory not found: {train_file_path}")
            return 
        
        #opens file, and uses safe_load to load it safely (external sources can nest system calls in yaml files)
        with open(train_file_path, 'r') as file_handler:
            images = yaml.safe_load(file_handler)
            #flattens out data, so we dont have dictionary of lists
            df = pd.json_normalize(
                images,
                record_path='boxes',
                meta=['path']
            )
            #renames the colum names to match with other datasets
            df = df.rename(columns={"x_min": "x1", "x_max": "x2" , "y_min": "y1", "y_max": "y2", })

            
            #path represents the image path, group represents a bucket holding each image with the same image path
            for path, group in df.groupby('path'):

                boxes = []
                labels = []
                # for every row in the group (bucket) extract the boxes label and label
                for _, row in group.iterrows():

                    x1 = float(row['x1'])
                    x2 = float(row['x2'])
                    y1 = float(row['y1'])
                    y2 = float(row['y2'])

                    if x2 <= x1 or y2 <= y1:
                        continue

                    image_labels = str(row['label']).lower()
                    label = self.parse_labels(image_labels)

                #add labels to boxes array
                    boxes.append([x1,y1, x2, y2])

                #appends label to labels array
                    labels.append(label)

                if len(boxes) == 0:
                    continue


                image_indv_path = os.path.join(self.yaml_path, path)

                if not os.path.exists(image_indv_path):
                    print(f"File not found: {image_indv_path}")
                    continue

                self.samples.append({
                    'image_path': image_indv_path,
                    'boxes' : boxes,
                    'labels' : labels
                })

                print(f"Loaded Labels from {file_name}")

    #convert label to red, green, yellow label
    def parse_labels(self, image_labels):
        if 'go' in image_labels or 'green' in image_labels:
            return 3
        elif 'warning' in image_labels or 'yellow' in image_labels:
            return 2
        elif 'stop' in image_labels or 'red' in image_labels:
            return 1
        else:
            return 0
    def __len__(self):
        return len(self.samples)

    def __getitem__(self, index):
        sample = self.samples[index]
        img = Image.open(sample['image_path'])

    


                



        
        
        
                    
 