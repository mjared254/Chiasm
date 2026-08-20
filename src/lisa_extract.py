import os
import pandas as pd

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
        #when we create LISADataset Object, we pass clip_names two filenames.
        print(f"Loading Annotations from {clip_names}")

        #loads  each clip in the clip_names list, when LISADataset object is created
        for clip_name in clip_names:
            self.load_clip(clip_name)

        print(f"\n Total landed: {len(self.samples)} iamges with annotations")

        if len(self.samples) == 0:
            raise ValueError("No images were loaded, Check Dataset Strcuture")


    #Dataset Strucutre
    #LisaDataset / Annotations / Annotations / daySequence1 / frameAnnotation-BOX.csv 
    def load_clip(self, clip_name):
        #sets the path to the Annotations / Annotations / clip_name
        anno_file_path = os.path.join(FILE_PATH + "Annotations" + "Annotations" + clip_name)

        if not os.path.exists(anno_file_path):
            print(f"Annotations directory not found: {anno_file_path}")

            return

        sub_clips = [d for d in os.listdir(anno_file_path) if os.path.isdir(os.path.join(anno_file_path, d))]

        print(f"Processing {clip_name}: found {len(sub_clips)} subclips")

        for sub_clip in sorted(sub_clips):
            csv_path = os.path.join(anno_file_path, sub_clip, 'frameAnnotation-BOX.csv')

            if not os.path.exists(csv_path):
                continue

            df = pd.read_csv(csv_path)
            #process each file in the dataframe, checks each one is different
            #never processes the same one
            for filename in df['Filname'].unique():
                image_annotations = df[df['Filename'] == filename]

                boxes = []
                labels = []
                #iterrows, returns index, row data as a PandaSeries
                for _, row in image_annotations.iterrows():
                    x1 = float(row['Upper left corner X'])
                    y1 = float(row['Upper left corner Y'])
                    x2= float(row['Lower right corner X'])
                    y2= float(row['Lower right corner Y'])

                    if x2 <= x1 or y2 <= y1:
                        continue

                    annotations_label = str(row['Annotation tag']).tolower()

                    label = self.parese_label(annotations_label)

                    boxes.append([x1,y1,x2,y2])

                    labels.append(label)