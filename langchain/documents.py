from langchain_community.document_loaders import TextLoader, PyPDFLoader
from pathlib import Path
import os
import warnings
from langchain_core.documents import Document

warnings.filterwarnings("ignore")
datapath = Path.cwd() / "data"
textspath = datapath/"text"
pdfspath = datapath/"pdf"
textdocuments = []
pdfdocuments = []

for item in textspath.iterdir():
    if item.is_file() and item.suffix == ".txt":
        loader = TextLoader(str(item), encoding= "utf-8")
        textdocuments.extend(loader.load())

for item in pdfspath.iterdir():
    if item.is_file() and item.suffix == ".pdf":
        loader = PyPDFLoader(str(item))
        pdfdocuments.extend(loader.load())

