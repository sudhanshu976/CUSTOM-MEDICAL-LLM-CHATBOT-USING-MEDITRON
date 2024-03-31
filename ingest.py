# Imports
import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.document_loaders import DirectoryLoader
from langchain.document_loaders import PyPDFLoader
from langchain.vectorstores import Qdrant


# Creating Embeddings
embeddings = SentenceTransformerEmbeddings(model_name="NeuML/pubmedbert-base-embeddings")
print(embeddings)

# Load Directory
loader = DirectoryLoader('data/', glob="**/*.pdf", show_progress=True, loader_cls=PyPDFLoader)
# ( folder_path , type of documents , show_progress in terminal , loader_class )
documents = loader.load()


# Text Splitting ( Converting into list )
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
# chunk_overlap is generally 1/10th of total chunk size
texts = text_splitter.split_documents(documents)


url = "http://localhost:6333/dashboard"
qdrant = Qdrant.from_documents(
    texts,
    embeddings,
    url=url,
    prefer_grpc=False,
    collection_name="vector_db"
)

print("Vector DB Successfully Created!")





