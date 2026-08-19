import os

#Filepath to LisaDataset Folder
FILE_PATH = '/Users/jaredmorales04/Chiasm/LisaDataset'

#Checks if the filepath exists
if not os.path.exists(FILE_PATH):
    raise FileNotFoundError(f"Incorrect File Path: {FILE_PATH}")
print(f"Dataset File was found at {FILE_PATH}")

#Handles the LisaDataset data
class LISADataset():

    def __init__(self, file_path, clip_names, transforms=None):
        self.file_path = file_path
        self.transforms = transforms
        self.samples = []

        print(f"Loading Annotations from {clip_names}")
    #
        for clip_name in clip_names:
            self.load_clip(clip_name)

        print(f"\n Total landed: {len(self.samples)} iamges with annotations")

        if len(self.samples) == 0:
            raise ValueError("No images were loaded, Check Dataset Strcuture")
        
    def load_clip(self, clip_name):
        anno_file_path = os.path.join(FILE_PATH + "Annotations" + "Annotations" + clip_name)

        if not os.path.exists(anno_file_path):
            print(f"Annotations directory not found: {anno_file_path}")

            sub_clips = [d for d in os.listdir(anno_file_path) if os.path.isdir(os.path.join(anno_file_path, d))]

            print(f"Processing {clip_name}: found {len(sub_clips)} subclips")

            for sub_clip in sorted(sub_clips):
                csv_path = os.path.join(anno_file_path, sub_clip, 'frameAnnotation-BOX.csv')