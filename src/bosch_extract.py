import os
import yaml

FILE_PATH = '/Users/jaredmorales04/Chiasm/dataset_train_rgb/dataset_train_rgb'

if not os.path.exists(FILE_PATH):
    raise FileNotFoundError(f"Incorrect FilePath: {FILE_PATH}")
print(f"Dataset was found at {FILE_PATH}")


class BOSCHDataset():
    def __init__(self, yaml_path, clip_names):
        self.yaml_path = yaml_path
        self.samples = []

        print(f"Loading Annotations from {clip_name}")

        for clip_name in clip_names:
            self.load_clip(clip_name)

        print(f"\n Total landed: {len(self.samples)} images with annotations")

        if len(self.samples) == 0:
            raise ValueError("No Images were loaded, check Dataset Structure")
        
    def load_clip(self, clip_name):
        train_file_path = os.path.join(FILE_PATH + "train.yaml")

        if not os.path.exists(train_file_path):
            print(f"Annoations directory not found: {train_file_path}")
            return 

        with open(train_file_path, 'rb') as file_handler:
            images = yaml.load(file_handler)

        if not images or not isinstance(images[0], dict) or 'path' not in images[0]:
            raise ValueError('Something seems wrong with this label-file: {}'.format(train_file_path))
        
        #abspath cleans up and normalizes the path, we are concatenating train_file_path + 'path' at images[i]
        for i in range(len(images)):
            images[i]['path'] = os.path.abspath(os.path.join(os.path.dirname(train_file_path), images[i]['path']))
            #checks for cases where x_min > x_max, this is incorrect.
            for j, box in enumerate(images[i]['boxes']):
                if box['x_min'] > box['x_max']:
                    images[i]['boxes'][j]['x_min'], images[i]['boxes'][j]['x_max'] = (images[i]['boxes'][j]['x_max'],
                                                                                      images[i]['boxes'][j]['x_min'])
                if box['y_min'] > box['y_max']:
                    images[i]['boxes'][j]['y_min'], images[i]['boxes'][j]['y_max'] = (images[i]['boxes'][j]['y_max'],
                                                                                      images[i]['boxes'][j]['y_min'])

                    
                    
 