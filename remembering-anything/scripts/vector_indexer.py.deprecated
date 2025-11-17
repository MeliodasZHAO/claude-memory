"""
Vector indexer for claude-memory skill.
"""

from pathlib import Path
from typing import List
import chromadb
from sentence_transformers import SentenceTransformer

class VectorIndexer:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.client = None
        self.collection = None
        self.model = None

    def initialize_db(self):
        """Initialize ChromaDB and embedding model."""
        self.client = chromadb.PersistentClient(path=self.db_path)
        self.collection = self.client.get_or_create_collection("notes")
        self.model = SentenceTransformer('BAAI/bge-m3')

    def index_chunks(self, chunks: List[dict]):
        """Index chunks into vector database."""
        if not self.collection or not self.model:
            raise RuntimeError("Database not initialized")

        ids = [f"chunk_{i}" for i in range(len(chunks))]
        documents = [c['content'] for c in chunks]
        metadatas = [c['metadata'] for c in chunks]
        embeddings = self.model.encode(documents, convert_to_tensor=False)

        self.collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings.tolist(),
            metadatas=metadatas
        )
