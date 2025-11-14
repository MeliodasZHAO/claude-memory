"""
Chunk schema definition for vector database.
"""

from typing import TypedDict, Optional

class Chunk(TypedDict):
    """Schema for a text chunk to be indexed."""
    content: str
    metadata: dict  # Must include: filename, filepath, chunk_id, chunk_type

def validate_chunk(chunk: dict) -> bool:
    """Validate chunk against schema."""
    if 'content' not in chunk or 'metadata' not in chunk:
        return False
    meta = chunk['metadata']
    required = ['filename', 'filepath', 'chunk_id', 'chunk_type']
    return all(field in meta for field in required)
