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
        train_file_path = os.path.join(FILE_PATH + "tain.yaml")

        if not os.path.exists(train_file_path):
            print(f"Annoations directory not found: {train_file_path}")
            return 

        with open(train_file_path, 'rb') as file_handler:
            images = yaml.load(file_handler)