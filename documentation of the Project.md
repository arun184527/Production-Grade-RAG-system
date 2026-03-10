i want to bulid the Production-Grade RAG module

Data Acquisition is the First Step
where i downloaded the zip file from "Plain Text Wikipedia 2020-11" from Wikipedia
the file contains of 650+ file that are in format of "JSON" 
the JSON file contains "id number", "Text","Titel".
 - Text is Main contains used for tokenization, embeddings, and retrieval.
 - Titel is Used as metadata this is helps for showing source of the answer
 - id number that is the Unique identifier for the article
this is the our base data for the Production Grade RAG Model


Dataset Exploration is the Next Step 
Where i created a Python script "explore_dataset.py"

Example file opened
Opening file: 00c2bfc7-57db-496e-9d5c-d62f8d8119e3.json
Total articles in this file: 9982

Inspecting one article
ID: 7751000
Title: M-137 (Michigan highway)
Text preview: M-137 was a state trunkline highway in the US state of Michigan that served as a spur route to the Interlochen Center for the Arts and Interlochen State Park. It started south of the park and ran nort

Article statistics
Number of articles: 9982
Average text length: 4007.775896613905
Longest article: 194969
Shortest article: 1

Data Cleaning
now next step is the present data cleaning here i thought the data is already present in the from of json data why i should clean it. it is well fromanted data
here comes the improts of the clean data and the uncleaned data 
Advantage of clean data is 
 - Improve Data Quality - Cleaning ensures that the text contains only meaningful content, which improves the overall dataset quality
 - Improve Embedding Quality - Cleaning ensures that embeddings are generated from informative sentences, leading to better vector representations
 - Better Retrieval Results - Cleaning the data improves retrieval accuracy because only relevant information is embedded and stored
 - Reduce Token Size and Storage - token count, embedding generation time, vector database size
 - Improve Chunking - After cleaning, every chunk contains useful contextual information, improving the quality of the retrieval step.
 - Prevent Errors in Processing - errors like - Encoding Errors are that errors tokenizer errors, unreadable text, embedding inconsistencies,
                                              - Token overflow LLMs and embedding models have token limits ex 500 tokens, if the text conten 20,000 characters then we get this error "Token limit exceeded" to prevent i have to  Clean and then chunk the text.
                                              - Empty or Invalid Text How to prevent this we can do in Filter empty articles this is done when we write the Python programming 
                                              - Unwanted Sections like References, category, External links,  
What Happens If Data Is Not Cleaned
 - Noisy Embeddings - These tokens do not represent knowledge, so the embedding becomes less meaningful
 - Incorrect Retrieval Results - 
 - Poor Chunk Quality - Chunk is useless but still becomes an embedding vector.
What are the Uncleaned data that Present in that JSON File 
 - [1] - Citation Markers
 - ==References== - Section Markup
 - Category:Flora of Madagascar - Category Tags
 - {{Infobox}} - Template Markup
 - [[Madagascar]] - Internal Links
 - <ref>Smith 2003</ref> - HTML or XML Tags
 - * Smith 2003 - Bibliographic Lists
 - ==Further reading== - Navigation Sections
 - __INDEX__ - Category Index Commands
 - *** - Repeated Formatting Characters

Created a Python script "clean_dataset.py"
Tasks
 - load JSON files
 - clean text
 - remove noise
 - filter short articles
 - save cleaned data