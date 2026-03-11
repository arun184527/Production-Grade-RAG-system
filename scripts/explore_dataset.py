import json
import os
current_dir = os.path.dirname(__file__)
data_folder = os.path.join(current_dir, "..", "data")
file_path = os.path.join(data_folder, "clean_wikipedia.jsonl")
print("Dataset path:", data_folder)
print("Opening file:", file_path)
with open(file_path, "r", encoding="utf-8") as f:
    preview = f.read(10000)
print("\nPreview of dataset:\n")
print(preview)
