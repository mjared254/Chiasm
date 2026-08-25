import os
import sys
import json

FILE_PATH = None

if not os.path.exists(FILE_PATH):
    raise FileNotFoundError(f"Incorrect File Path: {FILE_PATH}")
print(f"Dataset File was found at {FILE_PATH}")

class DTLDataset():
    def __init__(self, file_path, clip_names):
        self.file_path = file_path
        self.samples = []

        print(f"Loading Annotations from {clip_names}")

        for clip_name in clip_names:
            self.load_clip(clip_name)