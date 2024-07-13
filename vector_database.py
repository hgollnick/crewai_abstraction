import os

from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma

def generate_embeddings():
    return SentenceTransformerEmbeddings(model_name=os.getenv("EMBEDDINGS_MODEL"))


def create_vector_database(splited_docs):
    vectordb = Chroma.from_documents(splited_docs, generate_embeddings())

    return vectordb

