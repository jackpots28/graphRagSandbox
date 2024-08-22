from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Neo4jVector
from langchain_core.documents import Document
from langchain_text_splitters import CharacterTextSplitter
ollama_emb = OllamaEmbeddings(
    model="llama3.1",
)