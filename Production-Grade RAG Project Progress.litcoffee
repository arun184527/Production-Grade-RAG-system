Production-Grade RAG Project Progress
Day - 1 
 - Project Setup & Dataset Collection
 - Created the project repository
 - Designed the project folder structure
 - Downloaded the Plain Text Wikipedia 2020-11 dataset
 - Extracted the dataset from the zip file 
 - Verified that the dataset contains 650+ JSON files
Day - 2
 - Dataset Exploration
 - Built a script to explore the dataset
 - Loaded JSON files and inspected article structure
 - Printed a sample article to verify fields
 - Articles vary significantly in size
 - Some articles contain extremely short or irrelevant content
Day - 3
 - Data Cleaning
 - Built a data cleaning script for the Wikipedia dataset
 - Identified Wikipedia artifacts present in the text data
 - Removed citation markers such as [1], [23]
 - Removed section headings like ==References==, ==External Links==
 - Removed category tags such as Category:...
 - Removed templates and wiki tables ({{ }}, {| |})
 - Removed HTML tags and URLs
 - Converted internal wiki links [[link]] and [[link|text]] to plain text
 - Removed special wiki commands like __INDEX__
 - Normalized whitespace to improve text quality
 - Filtered out very short or empty articles
 - Saved cleaned dataset to the data/cleaned directory
Day - 4
 - Document Chunking
 - Designed a chunking strategy for long Wikipedia articles
 - Implemented chunking using a sliding window approach
 - Configured chunk size of 500 words with 100-word overlap
 - Ensured contextual continuity between chunks
 - Preserved metadata including doc_id and title for each chunk
 - Generated unique identifiers for each chunk (chunk_id)
 - Created chunked dataset for embedding generation
 - Saved chunked files to the data/chunks directory