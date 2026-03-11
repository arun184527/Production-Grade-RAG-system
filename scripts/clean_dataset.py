import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from libraries.data_cleaning import DatasetCleaner
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_FILE = os.path.join(BASE_DIR, "data", "simple_wikipedia.jsonl")
OUTPUT_FILE = os.path.join(BASE_DIR, "data", "clean_wikipedia.jsonl")
cleaner = DatasetCleaner(min_length=50)
cleaner.clean_jsonl(INPUT_FILE, OUTPUT_FILE)