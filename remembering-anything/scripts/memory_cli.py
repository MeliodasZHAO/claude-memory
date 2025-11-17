#!/usr/bin/env python3
"""
Command-line interface for memory management.
"""

import sys
import argparse
from pathlib import Path

# scripts -> remembering-anything -> claude-memory
SKILL_DIR = Path(__file__).parent.parent.parent
sys.path.insert(0, str(SKILL_DIR / "remembering-anything" / "scripts"))

from memory_manager import MemoryManager
from summary_engine import SummaryEngine

def main():
    parser = argparse.ArgumentParser(description='Memory CLI')
    parser.add_argument('command', choices=['stats', 'search', 'conflicts', 'unprocessed', 'export', 'list'])
    parser.add_argument('args', nargs='*')
    parser.add_argument('--type', choices=['fact', 'preference', 'experience'])

    args = parser.parse_args()

    mm = MemoryManager()
    se = SummaryEngine()

    if args.command == 'stats':
        stats = mm.get_statistics()
        print("\n[-] Memory Statistics:")
        for key, value in stats.items():
            print(f"    {key}: {value}")

    elif args.command == 'search':
        query = args.args[0] if args.args else ""
        results = mm.search_memories(query, args.type)
        print(f"\n[?] Search results for '{query}':")
        for r in results:
            print(f"    [{r['type']}] {r['content']}")

    elif args.command == 'conflicts':
        conflicts = mm.detect_conflicts()
        print(f"\n[!] Found {len(conflicts)} conflicts:")
        for c in conflicts:
            print(f"    {c['description']}")

    elif args.command == 'unprocessed':
        unprocessed = se.list_unprocessed_notes()
        print(f"\n[*] Unprocessed notes ({len(unprocessed)}):")
        for note in unprocessed:
            print(f"    {note}")

    elif args.command == 'export':
        output = args.args[0] if args.args else "backup.json"
        mm.export_memories(output)
        print(f"\n[v] Exported to {output}")

    elif args.command == 'list':
        mem_type = args.type or 'fact'
        if mem_type == 'fact':
            items = mm.get_active_facts()
        elif mem_type == 'preference':
            items = mm.get_active_preferences()
        else:
            items = mm.get_active_experiences()
        print(f"\n[-] Active {mem_type}s ({len(items)}):")
        for item in items:
            print(f"    [{item['category']}] {item['content']}")

if __name__ == "__main__":
    main()
