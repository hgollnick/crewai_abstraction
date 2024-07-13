import os
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_community.document_loaders import PyPDFLoader

def load_docs():  
  directory = os.getenv("DOCUMENTS_FOLDER")
  
  loader = DirectoryLoader(directory, glob="*.pdf", loader_cls=PyPDFLoader)
  documents = loader.load()
  print("\nNumber of documents loaded: " + str(len(documents)))
  
  return documents
