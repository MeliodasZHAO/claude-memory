"""
Memory schema definitions for AI Partner Chat.

Defines the data structures for facts, preferences, experiences, and conflicts.
"""

from typing import TypedDict, Optional, List, Literal
from datetime import datetime
import uuid


# Type definitions for memory entries

class BaseMemory(TypedDict):
    """Base memory structure shared by all memory types."""
    id: str
    type: Literal["fact", "preference", "experience"]
    content: str
    source: str  # Where this memory came from
    timestamp: str  # ISO format timestamp
    last_updated: str  # ISO format timestamp
    confidence: float  # 0.0 to 1.0
    status: Literal["active", "deprecated", "conflicted"]
    tags: List[str]

    # Memory layering fields
    importance: Literal["core", "active", "contextual", "archived"]  # Memory importance level
    context_tags: List[str]  # Trigger scenarios/topics (e.g., ["coding", "work"])
    access_count: int  # Number of times accessed
    last_accessed: Optional[str]  # Last access timestamp (ISO format)

    # Short-term memory fields
    expires_at: Optional[str]  # Expiration timestamp (ISO format), for short-term memories
    is_work_in_progress: bool  # Whether this is an ongoing task/project


class FactMemory(BaseMemory):
    """Memory representing a factual statement about the user."""
    type: Literal["fact"]
    category: str  # e.g., "location", "occupation", "education"
    supersedes: Optional[str]  # ID of fact this replaces


class PreferenceMemory(BaseMemory):
    """Memory representing a user preference or habit."""
    type: Literal["preference"]
    category: str  # e.g., "communication", "work_style", "food"
    strength: Literal["strong", "moderate", "weak"]


class ExperienceMemory(BaseMemory):
    """Memory representing an experience or event."""
    type: Literal["experience"]
    category: str  # e.g., "work", "education", "travel"
    date: Optional[str]  # When it happened
    outcome: Optional[str]  # Result or lesson learned


class ConflictReport(TypedDict):
    """Report of conflicting memories."""
    conflict_id: str
    memory_ids: List[str]
    conflict_type: Literal["contradiction", "update", "refinement"]
    description: str
    suggested_resolution: str
    confidence: float


class MemoryDatabase(TypedDict):
    """Complete memory database structure."""
    facts: dict[str, FactMemory]
    preferences: dict[str, PreferenceMemory]
    experiences: dict[str, ExperienceMemory]
    metadata: dict


# Helper functions

def create_memory_id() -> str:
    """Generate a unique memory ID."""
    return f"mem_{uuid.uuid4().hex[:12]}"


def get_current_timestamp() -> str:
    """Get current timestamp in ISO format."""
    return datetime.now().isoformat()


def validate_memory(memory: BaseMemory) -> bool:
    """
    Validate a memory entry.

    Args:
        memory: Memory to validate

    Returns:
        True if valid, False otherwise
    """
    required_fields = ["id", "type", "content", "source", "timestamp",
                      "confidence", "status", "tags"]

    for field in required_fields:
        if field not in memory:
            return False

    if memory["confidence"] < 0.0 or memory["confidence"] > 1.0:
        return False

    if memory["status"] not in ["active", "deprecated", "conflicted"]:
        return False

    if memory["type"] not in ["fact", "preference", "experience"]:
        return False

    return True
