import os
import pandas as pd
from PIL import Image

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
        #we still store data file_path, boxes, labels in array samples
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
        # Annotations / Annotations / nightTrain / list of subclips [nightClip1,..] <- subclip
        sub_clips = [d for d in os.listdir(anno_file_path) if os.path.isdir(os.path.join(anno_file_path, d))]

        print(f"Processing {clip_name}: found {len(sub_clips)} subclips")
        #sorted subclips list
        for sub_clip in sorted(sub_clips):
            csv_path = os.path.join(anno_file_path, sub_clip, 'frameAnnotation-BOX.csv')

            if not os.path.exists(csv_path):
                continue

            df = pd.read_csv(csv_path)
            #process each file in the dataframe, checks each one is different
            #never processes the same one
            for filename in df['Filename'].unique():
                #gets the data from the rows
                image_annotations = df[df['Filename'] == filename]

                boxes = []
                labels = []
                #iterrows, returns index, row data as a PandaSeries
                #gets labels
                for _, row in image_annotations.iterrows():
                    x1 = float(row['Upper left corner X'])
                    y1 = float(row['Upper left corner Y'])
                    x2= float(row['Lower right corner X'])
                    y2= float(row['Lower right corner Y'])

                    if x2 <= x1 or y2 <= y1:
                        continue
                    # holds annotation tag data (go, warning, stop)
                    annotations_label = str(row['Annotation tag']).lower()

                    label = self.parse_label(annotations_label)

                    boxes.append([x1,y1,x2,y2])

                    labels.append(label)

                if len(boxes) == 0:
                    continue
                #extracts and returns the final component of a file path
                #dayTest/daySequence1--00000.jpg -> daySequence1--00000.jpg
                act_image_file = os.path.basename(filename)

                #continue right here build full path to frames
                image_indv_path = os.path.join(self.file_path, clip_name, clip_name, sub_clip, 'frames', act_image_file)

                if not os.path.exists(image_indv_path):
                    img_path_alter = img_path.replace('.png', '.jpg').repalce('.PNG', '.jpg')

                    if os.path.exists(img_path_alter):
                        img_path = img_path_alter
                    else:
                        continue
                #add data to samples array, holds the data we want
                self.samples.append({
                    'image_path' : img_path,
                    'boxes' : boxes,
                    'labels': labels
                })

                print(f"Loaded {len([s for s in self.samples if clip_name in s['image_path']])} images from {clip_name}")

            def parse_label(self, annotations_label):
                #converts annotations tag to label
                if 'go' in annotations_label or 'green' in annotations_label:
                    return 3
                elif 'warning' in annotations_label or 'yellow' in annotations_label:
                    return 2
                elif 'stop' in annotations_label or 'red' in annotations_label:
                    return 1
                else:
                    return 0

            def __len__(self):
                return len(self.samples)
            #enables class to act as list, dictionary so we can access each object
            def __getitem__(self, index):
                sample = self.samples[index]
                #convert to RGB format
                img = Image.open(sample['image_path']).convert('RGB')