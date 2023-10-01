import edgedb
from langchain.embeddings import HuggingFaceEmbeddings, SentenceTransformerEmbeddings


embeddings = HuggingFaceEmbeddings(model_name="intfloat/multilingual-e5-large")

client = edgedb.create_async_client()
