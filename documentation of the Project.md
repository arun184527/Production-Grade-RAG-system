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

Dataset Exploration is the Next Step 
Where i created a Python script "explore_dataset.py" to open the file 
Dataset path: d:\Git_projects\Production_RAG_Project\scripts\..\data
Opening file: d:\Git_projects\Production_RAG_Project\scripts\..\data\simple_wikipedia.jsonl
Preview of dataset:
 {"id": "796322", "url": "https://simple.wikipedia.org/wiki/Vit%C3%B3ria%20F.C.", "title": "Vitória F.C.", "text": "Vitoria Futebol Clube is a Portuguese sports club from the city of Setubal. Popularly known as Vitoria de Setubal (), the club was born under the original name Sport Victoria from the ashes of the small Bonfim Foot-Ball Club.\nReferences\n20th-century establishments in Portugal\n1910 establishments in Europe\nPortuguese football clubs"}
 {"id": "464811", "url": "https://simple.wikipedia.org/wiki/Pope%20Shenouda%20III%20of%20Alexandria", "title": "Pope Shenouda III of Alexandria", "text": "Pope Shenouda III (3 August 1923 - 17 March 2012) was the 117th Pope of Alexandria & Patriarch of the See of St. Mark. His papacy lasted for forty years, four months, and four days from 14 November 1971 until his death on 17 March 2012.\nPope Shenouda III died on 17 March 2012 in Cairo, Egypt from respiratory and kidney failure, aged 88.\nReferences\nOther websites\nOfficial website\nPope Shenouda III - Coptic Orthodox Church Network: Biography, Online Books, and Audio Sermons\nSome Articles by Pope Shenouda III in English\nMore information about the life of Pope Shenouda III - from Saint Takla Haymanout the Ethiopian Church, Alexandria, Egypt\nCommon declaration of Pope Shenouda III and Pope Paul VI (1973)\nPope Shenouda III's story and life in Arabic and English\nPope Shenouda III's Life\n1923 births\n2012 deaths\nCopts\nDeaths from renal failure\nDeaths from respiratory failure\nPatriarchs"}


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

To prepare the dataset for the Retrieval-Augmented Generation system, a data cleaning pipeline was implemented.
Instead of writing the cleaning logic directly inside the project script, the preprocessing functionality was designed as a reusable Python library.
This approach improves:
 - code reusability
 - modular design
 - maintainability
 - scalability across multiple AI/ML projects
The project script simply calls the cleaning library, while the library itself contains the full preprocessing logic.
Cleaning Library - libraries/data_cleaning/cleaner.py
for cleaning Created a Python script "clean_dataset.py"
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
To maintain modularity and code reusability, the chunking functionality was implemented as a reusable Python library rather than embedding the logic directly inside the project script.
This design ensures that the chunking system can be reused across different datasets and AI pipelines.
Chunking Library - libraries/chunking/chunker.py 
for chunking Created a Python script "chunk_dataset.py"
chunk_size = 500
This size is chosen to balance:
 - semantic completeness
 - embedding efficiency
 - retrieval accuracy
Overlap = 50
The overlapping region ensures that context is preserved across chunks
Each chunk contains:
 - chunk_id – unique identifier for the chunk
 - title – article title used as metadata
 - text – the chunked portion of the article text

Embedding Generation 
After splitting the dataset into smaller text chunks, the next step in the Retrieval-Augmented Generation (RAG) pipeline is embedding generation.
Embedding models convert text into dense numerical vectors that capture the semantic meaning of the content. These vectors allow the system to perform semantic search, enabling the retrieval of relevant information based on meaning rather than exact keyword matching.
In this project, each chunk of text is transformed into an embedding vector and stored for later use in the vector database.
To maintain modularity and code reuse, the embedding functionality is implemented as a reusable Python library.
Embedding Library - libraries/embedding/embedder.py
for Embedding Created a python script "generate_embeddings.py"
Why Embeddings Are Important 
Embedding vectors allow the system to perform semantic search instead of keyword-based search

Embedding Model
The project uses the following embedding model
 - "sentence-transformers/all-MiniLM-L6-v2"
This model was chosen because
 - produces high-quality semantic embeddings
 - is lightweight and fast
 - is widely used in production RAG systems
 - works well for semantic search tasks
The model converts each text chunk into a 384-dimensional vector representation
Embedding Generation Process
 - Load the chunked dataset (wiki_chunks.jsonl)
 - Read each chunk line-by-line
 - Extract the text content
 - Generate an embedding vector using the embedding model
 - Attach the vector to the chunk metadata
 - Save the result to a new JSONL dataset
This approach ensures the pipeline can handle large datasets efficiently without exceeding memory limits
The embedding model converts the query into a vector
The system then searches the vector database to find chunks with similar vector representations, which likely contain the relevant information.
This allows the system to retrieve relevant knowledge even if the exact words in the query do not appear in the text.
Benefits of Using Embeddings
 - Enables semantic similarity search
 - Improves retrieval accuracy
 - Reduces dependency on keyword matching
 - Handles paraphrased queries effectively
 - Provides better context for LLM responses

Vector Database 
After generating embeddings for all text chunks, the next step is to store these embeddings in a vector database.
A vector database allows the system to perform fast similarity search between a user query and the stored embeddings.
Instead of scanning every document manually, the vector database finds the most similar vectors efficiently.
In this project i used 
FAISS - Facebook AI Similarity Search
 - extremely fast
 - memory efficient
 - optimized for high-dimensional vector search
 - scalable for millions of embeddings

Retriever Module
After building the vector database, the next critical component in the RAG system is the Retriever. The retriever is responsible for searching the vector database and selecting the most relevant information for a given user query.
In a Retrieval-Augmented Generation (RAG) system, the language model does not directly search through the entire dataset. Instead, the retriever finds the most relevant pieces of information from the knowledge base and provides them to the language model as context. This significantly improves answer accuracy and reduces hallucination.   
Role of the Retriever in the RAG Pipeline
The retriever opeates in the query pipeline, which begins when a user asks a question.
flow:
 User Question
 Query Embedding
 Vector Search (FAISS)
 Top-K Relevant Chunks
 Prompt Builder
 LLM Generates Answer
The retriever sits between the user query and the language model, acting as the system that retrieves the most relevant information from the knowledge base.
How the Retriever Works
 - User Query Input - The process starts when the user asks a question.
                    Example - Who invented the telephone?
 - Query Embedding - The retriever converts the user question into a vector using the same embedding model that was used during document indexing
                    Example - Text → Embedding Vector
 This ensures the query and stored documents are represented in the same vector space
 - Vector Similarity Search - The query vector is then searched against the vector database using FAISS
 FAISS calculates similarity between the query vector and stored document vectors using a distance metric (usually cosine similarity or Euclidean distance)
 The system returns the Top-K most similar document chunks
 - Retrieve Relevant Chunks - The retriever returns the corresponding text chunks and metadata (such as title or source URL) for the most relevant results.
 Example retrieved context
 Title: Telephone
 Text: Alexander Graham Bell invented the telephone in 1876
 These retrieved chunks become the context for the language model
Why the Retriever is Important
The retriever is one of the most important components in a RAG system because it determines what information the language model receives.
Without a retriever
 - The language model would rely only on its training data
 - It may produce hallucinated or outdated answers
 - It cannot access external knowledge sources
With a retriever
 - The system can search large knowledge bases
 - Answers are grounded in real documents
 - Hallucination is reduced
 - Responses become more accurate and reliable
Benefits of Using a Retriever
 - Enables semantic search across large document collections
 - Improves factual accuracy of generated answers
 - Allows the system to scale to large datasets
 - Keeps the language model focused on relevant information
 - Supports domain-specific knowledge retrieval
Retriever Output Example
 Input Query
Who invented the telephone?
Retrieved Results
 - Alexander Graham Bell invented the telephone in 1876
 - The telephone was patented by Alexander Graham Bell
 - Bell's invention revolutionized communication technology
These retrieved chunks are passed to the language model, which then generates the final answer
The retriever acts as the information retrieval engine of the RAG system. It efficiently searches the vector database, identifies the most relevant knowledge, and provides it to the language model as context. This step ensures that the generated answers are grounded in the underlying knowledge base rather than relying only on the model's internal knowledge.
