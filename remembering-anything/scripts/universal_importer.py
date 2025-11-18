#!/usr/bin/env python3
"""
Universal Importer - Import notes from various sources.

Supports:
- Obsidian vaults (Markdown with frontmatter)
- Notion exports (Markdown/CSV)
- Xiaomi Notes (exported Markdown)
- Plain Markdown files
- Text files
"""

import os
import re
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Tuple


class UniversalImporter:
    """Import notes from various formats."""

    def __init__(self):
        """Initialize the importer."""
        self.skill_dir = Path(__file__).parent.parent
        self.user_data = self.skill_dir / "user-data"
        self.notes_dir = self.user_data / "notes"
        self.import_log = []

    def import_from_path(self, source_path: str) -> Dict[str, Any]:
        """
        Import notes from a file or directory.
        Auto-detects format and processes accordingly.
        """
        source = Path(source_path)

        if not source.exists():
            return {
                'success': False,
                'error': f'Path not found: {source_path}',
                'imported': 0
            }

        # Detect source type
        source_type = self._detect_source_type(source)

        print(f"[i] Detected source type: {source_type}")

        # Import based on type
        if source_type == 'obsidian':
            return self._import_obsidian(source)
        elif source_type == 'notion':
            return self._import_notion(source)
        elif source_type == 'xiaomi':
            return self._import_xiaomi(source)
        elif source_type == 'markdown':
            return self._import_markdown(source)
        else:
            return self._import_generic(source)

    def _detect_source_type(self, path: Path) -> str:
        """Detect the source type based on file/folder structure."""
        if path.is_dir():
            # Check for Obsidian vault
            if (path / '.obsidian').exists():
                return 'obsidian'

            # Check for typical Notion export structure
            files = list(path.glob('*.md')) + list(path.glob('*.csv'))
            if files and any('Notion' in f.name or 'notion' in f.name for f in files):
                return 'notion'

            # Multiple markdown files
            md_files = list(path.glob('**/*.md'))
            if md_files:
                return 'markdown'

        elif path.is_file():
            # Check file content for format hints
            if path.suffix.lower() == '.md':
                content = path.read_text(encoding='utf-8', errors='ignore')

                # Obsidian has frontmatter
                if content.startswith('---\n'):
                    return 'obsidian'

                # Xiaomi notes often have specific patterns
                if '小米便签' in content or 'Mi Notes' in content:
                    return 'xiaomi'

                # Notion exports have specific patterns
                if 'Created:' in content or 'Last Edited:' in content:
                    return 'notion'

                return 'markdown'

            elif path.suffix.lower() in ['.txt', '.text']:
                return 'text'

        return 'generic'

    def _import_obsidian(self, path: Path) -> Dict[str, Any]:
        """Import Obsidian vault or files."""
        imported = 0
        errors = []

        # Get all markdown files
        if path.is_dir():
            md_files = list(path.glob('**/*.md'))
        else:
            md_files = [path]

        for md_file in md_files:
            # Skip hidden files and templates
            if md_file.name.startswith('.') or 'template' in md_file.name.lower():
                continue

            try:
                content = md_file.read_text(encoding='utf-8')

                # Parse frontmatter
                metadata = {}
                if content.startswith('---\n'):
                    end_idx = content.find('\n---\n', 4)
                    if end_idx > 0:
                        frontmatter = content[4:end_idx]
                        content = content[end_idx + 5:]

                        # Simple frontmatter parsing
                        for line in frontmatter.split('\n'):
                            if ':' in line:
                                key, value = line.split(':', 1)
                                metadata[key.strip()] = value.strip()

                # Process Obsidian links [[]]
                content = re.sub(r'\[\[([^\]]+)\]\]', r'\1', content)

                # Generate filename
                date_str = datetime.now().strftime('%Y%m%d_%H%M%S')
                new_filename = f"obsidian_{md_file.stem}_{date_str}.md"
                target_path = self.notes_dir / "imported" / new_filename

                # Add import metadata
                import_header = f"""---
imported_from: obsidian
imported_date: {datetime.now().isoformat()}
original_file: {md_file.name}
{self._format_metadata(metadata)}
---

"""
                # Save to notes directory
                target_path.parent.mkdir(parents=True, exist_ok=True)
                target_path.write_text(import_header + content, encoding='utf-8')

                imported += 1
                self.import_log.append(f"Imported: {md_file.name} -> {new_filename}")

            except Exception as e:
                errors.append(f"Error importing {md_file.name}: {str(e)}")

        return {
            'success': True,
            'imported': imported,
            'errors': errors,
            'log': self.import_log
        }

    def _import_notion(self, path: Path) -> Dict[str, Any]:
        """Import Notion export."""
        imported = 0
        errors = []

        # Get all files
        if path.is_dir():
            files = list(path.glob('**/*.md')) + list(path.glob('**/*.csv'))
        else:
            files = [path]

        for file in files:
            if file.suffix.lower() == '.md':
                try:
                    content = file.read_text(encoding='utf-8')

                    # Process Notion metadata
                    metadata = {}
                    lines = content.split('\n')
                    new_lines = []

                    for line in lines:
                        # Extract Notion metadata
                        if line.startswith('Created:'):
                            metadata['created'] = line.replace('Created:', '').strip()
                        elif line.startswith('Last Edited:'):
                            metadata['last_edited'] = line.replace('Last Edited:', '').strip()
                        elif line.startswith('Tags:'):
                            metadata['tags'] = line.replace('Tags:', '').strip()
                        else:
                            new_lines.append(line)

                    content = '\n'.join(new_lines)

                    # Generate filename
                    date_str = datetime.now().strftime('%Y%m%d_%H%M%S')
                    new_filename = f"notion_{file.stem}_{date_str}.md"
                    target_path = self.notes_dir / "imported" / new_filename

                    # Add import metadata
                    import_header = f"""---
imported_from: notion
imported_date: {datetime.now().isoformat()}
original_file: {file.name}
{self._format_metadata(metadata)}
---

"""
                    # Save
                    target_path.parent.mkdir(parents=True, exist_ok=True)
                    target_path.write_text(import_header + content, encoding='utf-8')

                    imported += 1
                    self.import_log.append(f"Imported: {file.name} -> {new_filename}")

                except Exception as e:
                    errors.append(f"Error importing {file.name}: {str(e)}")

        return {
            'success': True,
            'imported': imported,
            'errors': errors,
            'log': self.import_log
        }

    def _import_xiaomi(self, path: Path) -> Dict[str, Any]:
        """Import Xiaomi Notes export."""
        imported = 0
        errors = []

        # Xiaomi notes are usually in a single file or multiple markdown files
        if path.is_dir():
            files = list(path.glob('**/*.md'))
        else:
            files = [path]

        for file in files:
            try:
                content = file.read_text(encoding='utf-8')

                # Xiaomi notes might have date patterns
                date_pattern = r'(\d{4}[-/]\d{1,2}[-/]\d{1,2})'
                dates = re.findall(date_pattern, content)

                metadata = {}
                if dates:
                    metadata['note_date'] = dates[0]

                # Generate filename
                date_str = datetime.now().strftime('%Y%m%d_%H%M%S')
                new_filename = f"xiaomi_{file.stem}_{date_str}.md"
                target_path = self.notes_dir / "imported" / new_filename

                # Add import metadata
                import_header = f"""---
imported_from: xiaomi_notes
imported_date: {datetime.now().isoformat()}
original_file: {file.name}
{self._format_metadata(metadata)}
---

"""
                # Save
                target_path.parent.mkdir(parents=True, exist_ok=True)
                target_path.write_text(import_header + content, encoding='utf-8')

                imported += 1
                self.import_log.append(f"Imported: {file.name} -> {new_filename}")

            except Exception as e:
                errors.append(f"Error importing {file.name}: {str(e)}")

        return {
            'success': True,
            'imported': imported,
            'errors': errors,
            'log': self.import_log
        }

    def _import_markdown(self, path: Path) -> Dict[str, Any]:
        """Import generic Markdown files."""
        imported = 0
        errors = []

        if path.is_dir():
            md_files = list(path.glob('**/*.md'))
        else:
            md_files = [path]

        for md_file in md_files:
            try:
                content = md_file.read_text(encoding='utf-8')

                # Generate filename
                date_str = datetime.now().strftime('%Y%m%d_%H%M%S')
                new_filename = f"md_{md_file.stem}_{date_str}.md"
                target_path = self.notes_dir / "imported" / new_filename

                # Add import metadata
                import_header = f"""---
imported_from: markdown
imported_date: {datetime.now().isoformat()}
original_file: {md_file.name}
---

"""
                # Save
                target_path.parent.mkdir(parents=True, exist_ok=True)
                target_path.write_text(import_header + content, encoding='utf-8')

                imported += 1
                self.import_log.append(f"Imported: {md_file.name} -> {new_filename}")

            except Exception as e:
                errors.append(f"Error importing {md_file.name}: {str(e)}")

        return {
            'success': True,
            'imported': imported,
            'errors': errors,
            'log': self.import_log
        }

    def _import_generic(self, path: Path) -> Dict[str, Any]:
        """Import generic text files."""
        imported = 0
        errors = []

        if path.is_dir():
            files = list(path.glob('**/*'))
            files = [f for f in files if f.is_file()]
        else:
            files = [path]

        for file in files:
            # Skip non-text files
            if file.suffix.lower() not in ['.txt', '.text', '.md', '.markdown', '.log']:
                continue

            try:
                content = file.read_text(encoding='utf-8', errors='ignore')

                # Convert to markdown
                if not file.suffix.lower() in ['.md', '.markdown']:
                    content = f"```\n{content}\n```"

                # Generate filename
                date_str = datetime.now().strftime('%Y%m%d_%H%M%S')
                new_filename = f"imported_{file.stem}_{date_str}.md"
                target_path = self.notes_dir / "imported" / new_filename

                # Add import metadata
                import_header = f"""---
imported_from: generic
imported_date: {datetime.now().isoformat()}
original_file: {file.name}
file_type: {file.suffix}
---

"""
                # Save
                target_path.parent.mkdir(parents=True, exist_ok=True)
                target_path.write_text(import_header + content, encoding='utf-8')

                imported += 1
                self.import_log.append(f"Imported: {file.name} -> {new_filename}")

            except Exception as e:
                errors.append(f"Error importing {file.name}: {str(e)}")

        return {
            'success': True,
            'imported': imported,
            'errors': errors,
            'log': self.import_log
        }

    def _format_metadata(self, metadata: Dict[str, Any]) -> str:
        """Format metadata for frontmatter."""
        lines = []
        for key, value in metadata.items():
            if value:
                lines.append(f"{key}: {value}")
        return '\n'.join(lines)


def main():
    """Test the importer."""
    import sys
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    importer = UniversalImporter()

    print("=== 通用导入器测试 ===\n")
    print("支持的格式:")
    print("  - Obsidian vaults (带 frontmatter 的 Markdown)")
    print("  - Notion 导出 (Markdown/CSV)")
    print("  - 小米便签导出 (Markdown)")
    print("  - 普通 Markdown 文件")
    print("  - 文本文件\n")

    # Test with current directory
    test_path = input("请输入要导入的文件或文件夹路径 (按 Enter 跳过): ").strip()

    if test_path:
        print(f"\n开始导入: {test_path}")
        result = importer.import_from_path(test_path)

        print(f"\n导入结果:")
        print(f"  成功: {result['success']}")
        print(f"  导入文件数: {result['imported']}")

        if result.get('errors'):
            print(f"  错误:")
            for error in result['errors']:
                print(f"    - {error}")

        if result.get('log'):
            print(f"\n导入日志:")
            for log_entry in result['log'][:5]:  # Show first 5
                print(f"  - {log_entry}")
    else:
        print("已跳过导入测试")

    # Show where files are imported
    import_dir = importer.notes_dir / "imported"
    print(f"\n导入的文件保存在: {import_dir}")


if __name__ == "__main__":
    main()