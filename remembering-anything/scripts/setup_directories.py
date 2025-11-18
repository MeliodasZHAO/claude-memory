#!/usr/bin/env python3
"""
Initialize Claude Memory skill directory structure.

This script creates the necessary directory structure and copies template files
to set up the skill for first use.
"""

import os
import shutil
from pathlib import Path


def main():
    """Initialize the skill directory structure."""
    # Get the skill directory (remembering-anything root)
    # scripts -> remembering-anything
    skill_dir = Path(__file__).parent.parent
    user_data_dir = skill_dir / "user-data"

    print("[*] Initializing Claude Memory skill...")
    print(f"    Skill directory: {skill_dir}")
    print()

    # Create directory structure
    print("[+] Creating directory structure...")
    directories = [
        user_data_dir / "notes" / "daily",
        user_data_dir / "notes" / "topics",
        user_data_dir / "config",
        user_data_dir / "memory",
        user_data_dir / "summaries" / "monthly",
        user_data_dir / "summaries" / "topics",
        user_data_dir / "media" / "images",  # 添加 media 文件夹
    ]

    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
        print(f"    [OK] {directory.relative_to(skill_dir)}")

    print()

    # Copy template files if they don't exist
    print("[+] Setting up persona templates...")
    templates = [
        ("user-persona-template.md", "user-persona.md"),
        ("ai-persona-template.md", "ai-persona.md"),
    ]

    assets_dir = skill_dir / "assets"
    config_dir = user_data_dir / "config"

    for template_name, target_name in templates:
        source = assets_dir / template_name
        target = config_dir / target_name

        if target.exists():
            print(f"    [i] Already exists: {target.relative_to(skill_dir)}")
        else:
            if source.exists():
                shutil.copy(source, target)
                print(f"    [+] Created: {target.relative_to(skill_dir)}")
            else:
                print(f"    [!] Template not found: {source.relative_to(skill_dir)}")

    print()
    print("[v] Initialization complete!")
    print()
    print("[-] Next steps:")
    print(f"    1. Add your markdown notes to: {user_data_dir / 'notes'}")
    print(f"    2. Edit your personas in: {config_dir}")
    print()
    print("[i] Or simply tell Claude Code to initialize the skill for you!")


if __name__ == "__main__":
    main()
