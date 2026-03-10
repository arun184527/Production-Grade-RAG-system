import json
import os
current_dir = os.path.dirname(__file__)
data_folder = os.path.join(current_dir, "..", "data", "archive","enwiki20201020")
print("Dataset path:", data_folder)
files = os.listdir(data_folder)
file_path = os.path.join(data_folder, files[0])
print("Opening file:", files[0])
with open(file_path, "r", encoding="utf-8") as f:
    articles = json.load(f)
print("Total articles in this file:", len(articles))
print("\nInspecting one article:\n")
article = articles[0]
print("ID:", article["id"])
print("Title:", article["title"])
print("Text preview:", article["text"][:200])
lengths = []
for article in articles:
    lengths.append(len(article["text"]))
print("\nArticle statistics")
print("Number of articles:", len(articles))
print("Average text length:", sum(lengths) / len(lengths))
print("Longest article:", max(lengths))
print("Shortest article:", min(lengths))