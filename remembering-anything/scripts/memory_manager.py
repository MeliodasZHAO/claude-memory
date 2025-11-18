"""
Memory Manager for AI Partner Chat.

Handles structured memory operations: add, update, delete, query, and conflict detection.
"""

import json
import os
from pathlib import Path
from typing import Optional, List, Dict, Any
from datetime import datetime

from memory_schema import (
    MemoryDatabase,
    FactMemory,
    PreferenceMemory,
    ExperienceMemory,
    ConflictReport,
    create_memory_id,
    get_current_timestamp,
    validate_memory,
)


class MemoryManager:
    """Manage structured memories with versioning and conflict detection."""

    def __init__(self, memory_dir: Optional[str] = None):
        """
        Initialize memory manager.

        Args:
            memory_dir: Path to memory directory. If None, uses global path.
        """
        if memory_dir is None:
            # scripts -> remembering-anything
            skill_dir = Path(__file__).parent.parent
            memory_dir = skill_dir / "user-data" / "memory"

        self.memory_dir = Path(memory_dir)
        self.memory_dir.mkdir(parents=True, exist_ok=True)

        self.facts_file = self.memory_dir / "facts.json"
        self.preferences_file = self.memory_dir / "preferences.json"
        self.experiences_file = self.memory_dir / "experiences.json"
        self.metadata_file = self.memory_dir / "metadata.json"

        self._ensure_files()

    def _ensure_files(self):
        """Ensure all memory files exist."""
        for file_path in [self.facts_file, self.preferences_file, self.experiences_file]:
            if not file_path.exists():
                self._save_json(file_path, {})

        if not self.metadata_file.exists():
            self._save_json(self.metadata_file, {
                "created": get_current_timestamp(),
                "last_updated": get_current_timestamp(),
                "version": "1.0"
            })

    def _load_json(self, file_path: Path) -> Dict:
        """Load JSON file."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def _save_json(self, file_path: Path, data: Dict):
        """Save JSON file."""
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        # Update metadata
        metadata = self._load_json(self.metadata_file)
        metadata["last_updated"] = get_current_timestamp()
        if file_path != self.metadata_file:
            self._save_json(self.metadata_file, metadata)

    # ========== Add Operations ==========

    def add_fact(
        self,
        content: str,
        category: str,
        source: str,
        confidence: float = 1.0,
        tags: Optional[List[str]] = None,
        supersedes: Optional[str] = None,
        importance: str = "active",
        context_tags: Optional[List[str]] = None,
        attachments: Optional[List[str]] = None,
    ) -> str:
        """
        Add a new fact memory.

        Args:
            content: The fact content
            category: Category (location, occupation, education, etc.)
            source: Where this came from
            confidence: Confidence level (0.0-1.0)
            tags: Optional tags
            supersedes: ID of fact this replaces (will deprecate that fact)
            importance: Memory importance level (core, active, contextual, archived)
            context_tags: Context trigger tags (e.g., ["coding", "work"])

        Returns:
            Memory ID (or existing memory ID if duplicate found)
        """
        facts = self._load_json(self.facts_file)

        # Check for duplicate content
        for existing_id, existing_fact in facts.items():
            if (existing_fact["status"] == "active" and
                existing_fact["content"].strip().lower() == content.strip().lower() and
                existing_fact["category"] == category):
                # Found duplicate, return existing ID
                return existing_id

        memory_id = create_memory_id()
        timestamp = get_current_timestamp()

        fact: FactMemory = {
            "id": memory_id,
            "type": "fact",
            "category": category,
            "content": content,
            "source": source,
            "timestamp": timestamp,
            "last_updated": timestamp,
            "confidence": confidence,
            "status": "active",
            "supersedes": supersedes,
            "tags": tags or [],
            "importance": importance,
            "context_tags": context_tags or [],
            "access_count": 0,
            "last_accessed": None,
            "attachments": attachments,
        }

        facts[memory_id] = fact
        self._save_json(self.facts_file, facts)

        # Deprecate old fact if specified
        if supersedes:
            self.deprecate_memory(supersedes, "fact")

        return memory_id

    def add_preference(
        self,
        content: str,
        category: str,
        source: str,
        strength: str = "moderate",
        confidence: float = 1.0,
        tags: Optional[List[str]] = None,
        importance: str = "active",
        context_tags: Optional[List[str]] = None,
        attachments: Optional[List[str]] = None,
    ) -> str:
        """
        Add a new preference memory.

        Args:
            content: The preference content
            category: Category (communication, work_style, food, etc.)
            source: Where this came from
            strength: Preference strength (strong, moderate, weak)
            confidence: Confidence level (0.0-1.0)
            tags: Optional tags
            importance: Memory importance level (core, active, contextual, archived)
            context_tags: Context trigger tags (e.g., ["coding", "work"])

        Returns:
            Memory ID (or existing memory ID if duplicate found)
        """
        preferences = self._load_json(self.preferences_file)

        # Check for duplicate content
        for existing_id, existing_pref in preferences.items():
            if (existing_pref["status"] == "active" and
                existing_pref["content"].strip().lower() == content.strip().lower() and
                existing_pref["category"] == category):
                # Found duplicate, return existing ID
                return existing_id

        memory_id = create_memory_id()
        timestamp = get_current_timestamp()

        preference: PreferenceMemory = {
            "id": memory_id,
            "type": "preference",
            "category": category,
            "content": content,
            "strength": strength,
            "source": source,
            "timestamp": timestamp,
            "last_updated": timestamp,
            "confidence": confidence,
            "status": "active",
            "tags": tags or [],
            "importance": importance,
            "context_tags": context_tags or [],
            "access_count": 0,
            "last_accessed": None,
            "attachments": attachments,
        }

        preferences[memory_id] = preference
        self._save_json(self.preferences_file, preferences)

        return memory_id

    def add_experience(
        self,
        content: str,
        category: str,
        source: str,
        date: Optional[str] = None,
        outcome: Optional[str] = None,
        confidence: float = 1.0,
        tags: Optional[List[str]] = None,
        importance: str = "active",
        context_tags: Optional[List[str]] = None,
        attachments: Optional[List[str]] = None,
    ) -> str:
        """
        Add a new experience memory.

        Args:
            content: The experience content
            category: Category (work, education, travel, etc.)
            source: Where this came from
            date: When it happened (optional)
            outcome: Result or lesson learned
            confidence: Confidence level (0.0-1.0)
            tags: Optional tags
            importance: Memory importance level (core, active, contextual, archived)
            context_tags: Context trigger tags (e.g., ["coding", "work"])

        Returns:
            Memory ID (or existing memory ID if duplicate found)
        """
        experiences = self._load_json(self.experiences_file)

        # Check for duplicate content
        for existing_id, existing_exp in experiences.items():
            if (existing_exp["status"] == "active" and
                existing_exp["content"].strip().lower() == content.strip().lower() and
                existing_exp["category"] == category):
                # Found duplicate, return existing ID
                return existing_id

        memory_id = create_memory_id()
        timestamp = get_current_timestamp()

        experience: ExperienceMemory = {
            "id": memory_id,
            "type": "experience",
            "category": category,
            "content": content,
            "date": date,
            "source": source,
            "timestamp": timestamp,
            "last_updated": timestamp,
            "confidence": confidence,
            "status": "active",
            "tags": tags or [],
            "outcome": outcome,
            "importance": importance,
            "context_tags": context_tags or [],
            "access_count": 0,
            "last_accessed": None,
            "attachments": attachments,
        }

        experiences[memory_id] = experience
        self._save_json(self.experiences_file, experiences)

        return memory_id

    # ========== Query Operations ==========

    def get_memory(self, memory_id: str, memory_type: str) -> Optional[Dict]:
        """Get a specific memory by ID."""
        file_map = {
            "fact": self.facts_file,
            "preference": self.preferences_file,
            "experience": self.experiences_file,
        }

        if memory_type not in file_map:
            return None

        memories = self._load_json(file_map[memory_type])
        return memories.get(memory_id)

    def get_active_facts(self, category: Optional[str] = None) -> List[FactMemory]:
        """Get all active facts, optionally filtered by category."""
        facts = self._load_json(self.facts_file)
        active = [f for f in facts.values() if f["status"] == "active"]

        if category:
            active = [f for f in active if f["category"] == category]

        # Sort by timestamp (newest first)
        active.sort(key=lambda x: x["timestamp"], reverse=True)
        return active

    def get_active_preferences(self, category: Optional[str] = None) -> List[PreferenceMemory]:
        """Get all active preferences, optionally filtered by category."""
        prefs = self._load_json(self.preferences_file)
        active = [p for p in prefs.values() if p["status"] == "active"]

        if category:
            active = [p for p in active if p["category"] == category]

        active.sort(key=lambda x: x["timestamp"], reverse=True)
        return active

    def get_active_experiences(self, category: Optional[str] = None) -> List[ExperienceMemory]:
        """Get all active experiences, optionally filtered by category."""
        exps = self._load_json(self.experiences_file)
        active = [e for e in exps.values() if e["status"] == "active"]

        if category:
            active = [e for e in active if e["category"] == category]

        active.sort(key=lambda x: x["timestamp"], reverse=True)
        return active

    def search_memories(self, query: str, memory_type: Optional[str] = None) -> List[Dict]:
        """
        Search memories by content.

        Args:
            query: Search query
            memory_type: Optional filter by type (fact, preference, experience)

        Returns:
            List of matching memories
        """
        results = []
        query_lower = query.lower()

        file_map = {
            "fact": self.facts_file,
            "preference": self.preferences_file,
            "experience": self.experiences_file,
        }

        types_to_search = [memory_type] if memory_type else list(file_map.keys())

        for mem_type in types_to_search:
            memories = self._load_json(file_map[mem_type])
            for memory in memories.values():
                if memory["status"] != "active":
                    continue

                # Search in content and tags
                if (query_lower in memory["content"].lower() or
                    any(query_lower in tag.lower() for tag in memory.get("tags", []))):
                    results.append(memory)

        return results

    # ========== Update Operations ==========

    def update_fact(self, memory_id: str, **updates) -> bool:
        """Update a fact memory."""
        facts = self._load_json(self.facts_file)

        if memory_id not in facts:
            return False

        fact = facts[memory_id]
        for key, value in updates.items():
            if key in fact and key not in ["id", "type", "timestamp"]:
                fact[key] = value

        fact["last_updated"] = get_current_timestamp()
        self._save_json(self.facts_file, facts)
        return True

    def deprecate_memory(self, memory_id: str, memory_type: str) -> bool:
        """Mark a memory as deprecated."""
        file_map = {
            "fact": self.facts_file,
            "preference": self.preferences_file,
            "experience": self.experiences_file,
        }

        if memory_type not in file_map:
            return False

        memories = self._load_json(file_map[memory_type])

        if memory_id not in memories:
            return False

        memories[memory_id]["status"] = "deprecated"
        memories[memory_id]["last_updated"] = get_current_timestamp()
        self._save_json(file_map[memory_type], memories)
        return True

    def delete_memory(self, memory_id: str, memory_type: str) -> bool:
        """Permanently delete a memory."""
        file_map = {
            "fact": self.facts_file,
            "preference": self.preferences_file,
            "experience": self.experiences_file,
        }

        if memory_type not in file_map:
            return False

        memories = self._load_json(file_map[memory_type])

        if memory_id in memories:
            del memories[memory_id]
            self._save_json(file_map[memory_type], memories)
            return True

        return False

    # ========== Conflict Detection ==========

    def detect_conflicts(self) -> List[ConflictReport]:
        """
        Detect conflicting memories.

        Returns:
            List of conflict reports
        """
        conflicts = []

        # Check for contradictory facts in same category
        facts = self._load_json(self.facts_file)
        active_facts = [f for f in facts.values() if f["status"] == "active"]

        # Group by category
        by_category: Dict[str, List[FactMemory]] = {}
        for fact in active_facts:
            cat = fact["category"]
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append(fact)

        # Detect conflicts within categories that typically have single values
        single_value_categories = ["location", "occupation", "current_city", "current_company"]

        for category in single_value_categories:
            if category in by_category and len(by_category[category]) > 1:
                # Multiple active facts in single-value category
                facts_in_cat = by_category[category]
                conflicts.append({
                    "conflict_id": f"conflict_{create_memory_id()}",
                    "memory_ids": [f["id"] for f in facts_in_cat],
                    "conflict_type": "contradiction",
                    "description": f"Multiple active facts in '{category}' category",
                    "suggested_resolution": "Keep the most recent or highest confidence entry",
                    "confidence": 0.9,
                })

        return conflicts

    # ========== Layered Memory Operations ==========

    def get_core_memories(self) -> Dict[str, List[Dict]]:
        """
        Get core memories (importance='core') across all types.
        These are loaded on activation.

        Returns:
            Dict with keys: facts, preferences, experiences
        """
        facts = self._load_json(self.facts_file)
        prefs = self._load_json(self.preferences_file)
        exps = self._load_json(self.experiences_file)

        return {
            "facts": [f for f in facts.values()
                     if f["status"] == "active" and f.get("importance") == "core"],
            "preferences": [p for p in prefs.values()
                          if p["status"] == "active" and p.get("importance") == "core"],
            "experiences": [e for e in exps.values()
                          if e["status"] == "active" and e.get("importance") == "core"],
        }

    def get_memories_by_importance(self, importance_level: str) -> Dict[str, List[Dict]]:
        """
        Get memories by importance level.

        Args:
            importance_level: core, active, contextual, or archived

        Returns:
            Dict with keys: facts, preferences, experiences
        """
        facts = self._load_json(self.facts_file)
        prefs = self._load_json(self.preferences_file)
        exps = self._load_json(self.experiences_file)

        return {
            "facts": [f for f in facts.values()
                     if f["status"] == "active" and f.get("importance") == importance_level],
            "preferences": [p for p in prefs.values()
                          if p["status"] == "active" and p.get("importance") == importance_level],
            "experiences": [e for e in exps.values()
                          if e["status"] == "active" and e.get("importance") == importance_level],
        }

    def query_by_context(self, context_tags: List[str], limit: int = 5) -> List[Dict]:
        """
        Query memories by context tags.
        Used for triggered recall based on conversation topics.

        Args:
            context_tags: List of context tags to match (e.g., ["coding", "work"])
            limit: Maximum number of results to return

        Returns:
            List of matching memories, sorted by relevance
        """
        results = []

        # Search across all memory types
        for file_path in [self.facts_file, self.preferences_file, self.experiences_file]:
            memories = self._load_json(file_path)

            for memory in memories.values():
                if memory["status"] != "active":
                    continue

                # Check if any context_tag matches
                mem_context_tags = memory.get("context_tags", [])
                if any(tag in mem_context_tags for tag in context_tags):
                    results.append(memory)

        # Sort by access_count (most accessed first) and limit
        results.sort(key=lambda x: x.get("access_count", 0), reverse=True)
        return results[:limit]

    def mark_accessed(self, memory_id: str, memory_type: str):
        """
        Mark a memory as accessed (updates access_count and last_accessed).

        Args:
            memory_id: Memory ID
            memory_type: fact, preference, or experience
        """
        file_map = {
            "fact": self.facts_file,
            "preference": self.preferences_file,
            "experience": self.experiences_file,
        }

        if memory_type not in file_map:
            return

        memories = self._load_json(file_map[memory_type])

        if memory_id in memories:
            memories[memory_id]["access_count"] = memories[memory_id].get("access_count", 0) + 1
            memories[memory_id]["last_accessed"] = get_current_timestamp()
            self._save_json(file_map[memory_type], memories)

    def auto_maintain_importance(self, days_active: int = 7, days_contextual: int = 30):
        """
        Automatically maintain memory importance levels based on access patterns.

        Args:
            days_active: Days threshold for active memories
            days_contextual: Days threshold for contextual memories
        """
        from datetime import datetime, timedelta

        now = datetime.now()
        active_threshold = now - timedelta(days=days_active)
        contextual_threshold = now - timedelta(days=days_contextual)

        for file_path in [self.facts_file, self.preferences_file, self.experiences_file]:
            memories = self._load_json(file_path)
            updated = False

            for mem_id, memory in memories.items():
                if memory["status"] != "active":
                    continue

                # Skip core memories (never auto-demote)
                if memory.get("importance") == "core":
                    continue

                last_accessed = memory.get("last_accessed")
                access_count = memory.get("access_count", 0)

                # If never accessed, use timestamp
                if not last_accessed:
                    last_accessed = memory.get("timestamp")

                if last_accessed:
                    last_dt = datetime.fromisoformat(last_accessed)

                    # Promote to active if accessed frequently within days_active
                    if last_dt >= active_threshold and access_count >= 3:
                        if memory.get("importance") != "active":
                            memory["importance"] = "active"
                            updated = True

                    # Demote to contextual if not accessed within days_active
                    elif last_dt < active_threshold and memory.get("importance") == "active":
                        memory["importance"] = "contextual"
                        updated = True

                    # Archive if not accessed within days_contextual
                    elif last_dt < contextual_threshold and memory.get("importance") == "contextual":
                        memory["importance"] = "archived"
                        updated = True

            if updated:
                self._save_json(file_path, memories)

    # ========== Utility Functions ==========

    def get_all_categories(self, memory_type: str) -> List[str]:
        """Get all unique categories for a memory type."""
        file_map = {
            "fact": self.facts_file,
            "preference": self.preferences_file,
            "experience": self.experiences_file,
        }

        if memory_type not in file_map:
            return []

        memories = self._load_json(file_map[memory_type])
        categories = set(m["category"] for m in memories.values())
        return sorted(list(categories))

    def export_memories(self, output_file: str):
        """Export all memories to a single JSON file."""
        export_data = {
            "facts": self._load_json(self.facts_file),
            "preferences": self._load_json(self.preferences_file),
            "experiences": self._load_json(self.experiences_file),
            "metadata": self._load_json(self.metadata_file),
        }

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2)

    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about stored memories."""
        facts = self._load_json(self.facts_file)
        prefs = self._load_json(self.preferences_file)
        exps = self._load_json(self.experiences_file)

        return {
            "total_facts": len(facts),
            "active_facts": len([f for f in facts.values() if f["status"] == "active"]),
            "total_preferences": len(prefs),
            "active_preferences": len([p for p in prefs.values() if p["status"] == "active"]),
            "total_experiences": len(exps),
            "active_experiences": len([e for e in exps.values() if e["status"] == "active"]),
            "fact_categories": len(set(f["category"] for f in facts.values())),
            "last_updated": self._load_json(self.metadata_file).get("last_updated"),
        }
