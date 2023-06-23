import chromadb
import chromadb.config
from chromadb.server.fastapi import FastAPI

settings = chromadb.config.Settings(
    chroma_db_impl = "duckdb+parquet",
    persist_directory = "chroma_data"
)

server = FastAPI(settings)
app = server.app