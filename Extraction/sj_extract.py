import os

FILE_PATH = '/Users/jaredmorales04/Chiasm/SJ2TLDD'

if not os.path.exist(FILE_PATH):
	raise FileNotFoundError(f"Incorrect File Path: {FILE_PATH}")
print(f"Dataset File was found at {FILE_PATH}")


class SJ2TLDD():
	def __init__(self, xml_path, files):
		self.xml_path = xml_path
		self.samples = []

		print(f"Loading Annotations from {files}")

		for file in files:
			self.load_clip(file)

		print(f"\n Total landed: {len(self.samples)} images annotations")

		if len(self.samples) == 0:
			raise ValueError("No images were landed, Check Dataset Structure")

	def load_clip(self, file):
		xml_path_join = os.path.join(FILE_PATH, file )