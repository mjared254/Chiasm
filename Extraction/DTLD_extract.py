import os
import sys
import json
import pandas as pd

FILE_PATH = '/Users/jaredmorales04/Chiasm/DriveUDataset'

if not os.path.exists(FILE_PATH):
    raise FileNotFoundError(f"Incorrect File Path: {FILE_PATH}")
print(f"Dataset File was found at {FILE_PATH}")

class DTLDataset():
    def __init__(self, file_path, file_directory):
        self.file_path = file_path
        self.samples = []

        print(f"Loading Annotations from {file_name}")

        for file_name in file_directory:
            self.load_clip(file_name)

        print(f"Total landed: {len(self.samples)} images from annotations")

    def load_clip(self, file_name):
        dtld_file_path = os.path.join(FILE_PATH, file_name)

        if not os.path.exists(dtld_file_path):
            print(f"Annotations directory not found: {dtld_file_path}")
            return

        sub_files = [j for j in os.listdir(dtld_file_path) if os.path.isdir(os.path.join(dtld_file_path, j))]

        for sub_file in sub_files:
            with open(dtld_file_path, 'r') as file_handler:
                data = json.load(file_handler)


                df = pd.json_normalize(
                    data,
                    record_path=['attributes'],
                    sep = ","
                )