"""
Summary Engine for AI Partner Chat - provides framework for memory extraction.
"""

import json
from pathlib import Path
from typing import List, Dict, Optional, Any
from datetime import datetime

SUMMARY_INSTRUCTIONS = """
# Memory Extraction Instructions
Extract facts, preferences, and experiences from notes.
Detect conflicts with existing memories.
Return structured JSON format.
"""

class SummaryEngine:
    def __init__(self, notes_dir: Optional[str] = None, memory_dir: Optional[str] = None):
        skill_dir = Path(__file__).parent.parent
        self.notes_dir = Path(notes_dir) if notes_dir else skill_dir / "user-data" / "notes"
        self.memory_dir = Path(memory_dir) if memory_dir else skill_dir / "user-data" / "memory"
        self.summaries_dir = skill_dir / "user-data" / "summaries"
        self.summaries_dir.mkdir(parents=True, exist_ok=True)

    def get_instruction_prompt(self) -> str:
        return SUMMARY_INSTRUCTIONS

    def list_notes(self, pattern: str = "**/*.md") -> List[Path]:
        if not self.notes_dir.exists():
            return []
        return sorted(self.notes_dir.glob(pattern))

    def list_unprocessed_notes(self) -> List[Path]:
        log_file = self.memory_dir / "processing_log.json"
        processed = {}
        if log_file.exists():
            with open(log_file, "r", encoding="utf-8") as f:
                processed = json.load(f)

        all_notes = self.list_notes()
        unprocessed = []
        for note_path in all_notes:
            note_str = str(note_path)
            last_modified = note_path.stat().st_mtime
            if note_str not in processed or processed[note_str] < last_modified:
                unprocessed.append(note_path)
        return unprocessed

    def mark_note_processed(self, note_path: Path):
        log_file = self.memory_dir / "processing_log.json"
        processed = {}
        if log_file.exists():
            with open(log_file, "r", encoding="utf-8") as f:
                processed = json.load(f)
        processed[str(note_path)] = note_path.stat().st_mtime
        with open(log_file, "w", encoding="utf-8") as f:
            json.dump(processed, f, ensure_ascii=False, indent=2)

    def save_summary(self, content: str, summary_type: str = "monthly"):
        timestamp = datetime.now()
        if summary_type == "monthly":
            filename = f"{timestamp.strftime('%Y-%m')}.md"
            summary_path = self.summaries_dir / "monthly"
        else:
            filename = f"{summary_type}_{timestamp.strftime('%Y%m%d')}.md"
            summary_path = self.summaries_dir / "topics"
        summary_path.mkdir(parents=True, exist_ok=True)
        output_file = summary_path / filename
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(content)
        return output_file
