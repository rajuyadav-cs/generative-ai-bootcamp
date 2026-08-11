import warnings
warnings.simplefilter("ignore")

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from pathlib import Path
import os 
import torch

# print("CUDA available:", torch.cuda.is_available())

# if torch.cuda.is_available():
#     print("GPU:", torch.cuda.get_device_name(0))



home = Path(Path.cwd())
data = home / "data"
pdfspath = data / "pdf"
textspath = data/ "text"
# print(str(pdfspath))

pdflist = pdfspath.glob("*.pdf")
documents = []

for file in pdflist:
    
    if file.is_file():
        pdfloader = PyPDFLoader(file_path= str(file))
        documents.extend(pdfloader.load())

splitter = RecursiveCharacterTextSplitter(
    chunk_size = 250,
    chunk_overlap = 50,
    separators=["\n\n", "\n", " ", ""]
)        

splitted_pdfs = splitter.split_documents(documents)

# for chunk in splitted_pdfs[0:10]:
#     print(f"Page Content : \n{chunk.page_content}\n\nMeta Data : \n{chunk.metadata}")
#     print("--------------------------------") 
    
# ---------------------------Embedding Model------------
warnings.filterwarnings("ignore")
from langchain_huggingface import HuggingFaceEmbeddings

embedding = HuggingFaceEmbeddings(
    model_name = "sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs = {"device": "cuda"}
)    

text = "LangChain is used to build LLM applications."

vector = embedding.embed_query(text)

pdftextslist = [doc.page_content for doc in splitted_pdfs]

embeddedpdfs = embedding.embed_documents(pdftextslist)

# print("Number of chunks:", len(embeddedpdfs))
# print("Vector dimension:", len(embeddedpdfs[0]))
# print("Vector type:", type(embeddedpdfs[0]))
# print("First 5 values:", embeddedpdfs[0][:5])
