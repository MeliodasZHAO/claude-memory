"""
Note search utilities using Claude Code's native tools.

This module provides note search functionality without requiring
vector databases or embedding models. It leverages Claude's ability
to use Grep and Read tools directly.

Usage in SKILL.md:
    When user asks to search notes, use:
    - Grep tool to find files containing keywords
    - Read tool to read the full content
    - Claude's understanding to rank by relevance
"""

from pathlib import Path
from typing import List, Dict, Optional


def get_notes_dir() -> Path:
    """Get the global notes directory path."""
    # scripts -> remembering-anything -> claude-memory -> user-data
    skill_dir = Path(__file__).parent.parent.parent
    return skill_dir / "user-data" / "notes"


def get_all_notes() -> List[Path]:
    """
    Get all markdown note files.

    Returns:
        List of Path objects for all .md files in notes directory
    """
    notes_dir = get_notes_dir()
    if not notes_dir.exists():
        return []
    return list(notes_dir.glob("**/*.md"))


def format_note_info(note_path: Path) -> Dict[str, str]:
    """
    Format note file information.

    Args:
        note_path: Path to note file

    Returns:
        Dict with filename, relative_path, full_path
    """
    notes_dir = get_notes_dir()
    return {
        'filename': note_path.name,
        'relative_path': str(note_path.relative_to(notes_dir)),
        'full_path': str(note_path),
    }


# Note: For actual search, Claude agent should use:
# 1. Grep tool to search for keywords in notes directory
# 2. Read tool to read matching files
# 3. Claude's understanding to determine relevance and extract key info
#
# Example workflow in SKILL.md:
# ```
# User: "搜索关于项目的笔记"
# Agent:
#   1. Use Grep(pattern="项目", path="user-data/notes", output_mode="files_with_matches")
#   2. For each matched file, use Read() to get content
#   3. Analyze and summarize relevant information
#   4. Present results naturally (not as "查询到3条记录")
# ```
