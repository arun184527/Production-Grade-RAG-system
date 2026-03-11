i want to bulid the Production-Grade RAG module

Data Acquisition is the First Step
where i downloaded the dataset from "https://huggingface.co/datasets/pszemraj/simple_wikipedia"
the file name is simple_wikipedia file that is in format of "JSONl" 
the JSONl file contains "id number", "Url", Text","Titel".
 - Text is Main contains used for tokenization, embeddings, and retrieval.
 - Titel is Used as metadata this is helps for showing source of the answer
 - URL is Direct link to the original Wikipedia page 
 - id number that is the Unique identifier for the article
this is the our base data for the Production Grade RAG Model
Data Format 
 - Each line represents one independent JSON object
 - The dataset can be processed line-by-line without loading the entire file into memory
 {
"id": "796322",
"url": "https://simple.wikipedia.org/wiki/Vitória%20F.C.",
"title": "Vitória F.C.",
"text": "Vitoria Futebol Clube is a Portuguese sports club..."
}
here this file we can't download 


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
Cleaning Pipeline Implementation
 - Remove citation markers
 - Remove section headers
 - Remove category tags
 - Remove Wikipedia templates
 - Remove wiki tables
 - Remove HTML tags
 - Remove URLs
 - Convert wiki links to plain text
 - Remove bullet formatting while keeping content
 - Remove table formatting symbols
 - Remove special wiki commands
 - Normalize whitespace

Dataset Validation
After cleaning the dataset, a validation step was performed to ensure the preprocessing pipeline worked correctly
 - rticle structure consistency
 - removal of Wikipedia markup artifacts
 - minimum text length requirements
 - preservation of meaningful natural language content
 
Document Chunking
 Chunking means splitting long documents into smaller pieces so they can be processed by embedding models and stored efficiently in a vector database.
 Chunking acts as the bridge between raw textual data and embedding generation.
overlap - Overlap ensures that context is not lost between chunks.
Why Chunking Is Required
 Embedding models and language models have input size limitations. Long articles can exceed these limits or produce less accurate embeddings.
Benefits of chunking 
 - Improved Embedding Quality - Embedding models produce better vector representations when processing smaller, focused text segments.
 - Better Retrieval Accuracy - Instead of retrieving an entire article, the system retrieves the most relevant chunk, improving answer accuracy.
 - Efficient Vector Storage - Smaller chunks reduce memory overhead and make vector search more efficient.
 - Context Preservation - Using overlapping chunks ensures that contextual information is not lost between segments.
Chunking Workflow
 - Load cleaned Wikipedia articles.
 - Extract article metadata (ID and title).
 - Split article text into words.
 - Generate chunks of fixed size.
 - Apply overlapping windows to preserve context.
 - Store each chunk with metadata.
 - Save chunked data into a new dataset.
Result 
 - Long documents are converted into smaller semantic units.
 - Each chunk contains contextual information with overlap.
 - The dataset becomes suitable for embedding generation and vector search.

What Is an Embedding
 An embedding is a numerical vector representation of text
here i used the Sentence Transformers for Embedding
  