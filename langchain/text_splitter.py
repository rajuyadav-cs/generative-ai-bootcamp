from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


# print(type(pdfdocuments[1].page_content))        
page_content = """Haan, exactly. Agar goal **job/internship + strong projects** hai, toh tumhe LangChain ka har topic nahi padhna. Tumhe woh topics chahiye jo **actual AI Engineer/GenAI projects mein use hote hain**.

Main tumhe **Professional LangChain Roadmap** dungi — unnecessary cheezein hata ke.

### 🚀 Zero → Job Ready LangChain Roadmap

**1. LLM Fundamentals**

* LLM kya hai
* Tokens & context window
* Temperature
* System/User messages
* Model parameters
* API usage
* Streaming

**2. LangChain Core ⭐**

* Chat Models
* Messages
* Prompt Templates
* Structured Output
* Output Parsers
* Runnables
* LCEL
* `invoke()`
* `stream()`
* `batch()`
* RunnableSequence
* RunnableParallel
* RunnableLambda

**3. Prompt Engineering ⭐**

* System prompts
* Few-shot prompting
* Dynamic prompts
* Prompt variables
* Structured JSON output
* Prompt design for RAG/Agents

**4. Documents + Embeddings ⭐⭐⭐**

* Document loaders
* PDF/Web/CSV loading
* Document objects
* Metadata
* Text splitting
* Chunking strategy
* Embeddings
* Vector similarity

**5. Vector Databases ⭐⭐⭐**
At least **one properly** learn:

* Chroma
* FAISS
* Pinecone/Qdrant

Learn:

* Insert/upsert
* Similarity search
* Metadata filtering
* Top-K
* MMR

**6. RAG ⭐⭐⭐⭐⭐**
Ye sabse important hai.

* RAG architecture
* Indexing
* Retrieval
* Retriever
* `create_retrieval_chain`
* Context injection
* RAG prompting
* Conversational RAG
* Metadata filtering
* Multi-query retrieval
* Hybrid search
* Reranking
* Contextual compression
* RAG evaluation

**7. Tools ⭐⭐⭐⭐**

* `@tool`
* Custom tools
* Tool schema
* Tool calling
* Multiple tools
* Tool errors
* APIs ko tools banana

Example:

`search_web()`

`get_weather()`

`query_database()`

`send_email()`


"""
metadata = {"source": "textfile","author":"ruuh", "extension": ".txt"}

document = Document(page_content=page_content, metadata= metadata)
# print(type(document))

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 50,
    chunk_overlap = 5,
    separators=["\n\n", "\n", " ", ""], 
)

textchunks = text_splitter.split_text(document.page_content)
documentchunks = text_splitter.split_documents([document])

for chunk in textchunks:
    print(chunk)
    print("--------------------------------\n")
    break


for chunk in documentchunks[:5]:
    print(chunk)

print("---------------------------\n")
    

print(len(textchunks))
print(len(documentchunks))

print(type(textchunks[0]))
print(type(documentchunks[0]))

print(documentchunks[0].metadata)    