#!/usr/bin/env python3
"""
Build vector database from notes.
Claude Code should analyze note format and generate custom chunking logic.
"""

import sys
from pathlib import Path

SKILL_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(SKILL_DIR / "scripts"))

from chunk_schema import Chunk, validate_chunk
from vector_indexer import VectorIndexer

def chunk_note_file(filepath: str) -> list[Chunk]:
    """
    Analyze file and generate chunks.
    This function should be dynamically created by Claude Code
    based on actual note format.
    """
    chunks = []
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Simple paragraph-based chunking (example)
    paragraphs = content.split('\n\n')
    for i, para in enumerate(paragraphs):
        if len(para.strip()) < 50:
            continue
        chunk: Chunk = {
            'content': para.strip(),
            'metadata': {
                'filename': Path(filepath).name,
                'filepath': filepath,
                'chunk_id': i,
                'chunk_type': 'paragraph',
                'tags': [],
            }
        }
        if validate_chunk(chunk):
            chunks.append(chunk)
    return chunks

def main():
    USER_DATA = SKILL_DIR / "user-data"
    notes_dir = USER_DATA / "notes"
    db_path = str(USER_DATA / "vector_db")

    print("📦 Building vector database...")
    print(f"   Notes: {notes_dir}")
    print(f"   DB: {db_path}\n")

    indexer = VectorIndexer(db_path=db_path)
    indexer.initialize_db()

    all_chunks = []
    note_files = list(notes_dir.glob("**/*.md"))

    if not note_files:
        print("⚠️  No notes found")
        return

    for note_file in note_files:
        print(f"   Processing: {note_file.relative_to(notes_dir)}")
        try:
            chunks = chunk_note_file(str(note_file))
            all_chunks.extend(chunks)
            print(f"      ✓ {len(chunks)} chunks")
        except Exception as e:
            print(f"      ✗ Error: {e}")

    if all_chunks:
        print(f"\n📊 Total: {len(all_chunks)} chunks")
        print("🔄 Indexing...")
        indexer.index_chunks(all_chunks)
        print("✅ Done!\n")
    else:
        print("⚠️  No chunks generated\n")

if __name__ == "__main__":
    main()
