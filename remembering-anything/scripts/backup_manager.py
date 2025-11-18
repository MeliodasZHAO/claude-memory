#!/usr/bin/env python3
"""
Backup Manager - Export and backup all memories.

Features:
- Full backup of all memory data
- Incremental backups
- Export to different formats (JSON, Markdown)
- Restore from backup
"""

import json
import shutil
import zipfile
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional


class BackupManager:
    """Manage memory backups and exports."""

    def __init__(self):
        """Initialize backup manager."""
        self.skill_dir = Path(__file__).parent.parent
        self.user_data = self.skill_dir / "user-data"
        self.backup_dir = self.user_data / "backups"
        self.backup_dir.mkdir(exist_ok=True)

    def create_full_backup(self, description: str = "") -> Path:
        """Create a complete backup of all user data."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_name = f"backup_full_{timestamp}.zip"
        backup_path = self.backup_dir / backup_name

        # Create backup metadata
        metadata = {
            'timestamp': datetime.now().isoformat(),
            'type': 'full',
            'description': description,
            'version': '1.0'
        }

        # Create zip archive
        with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Add metadata
            zipf.writestr('backup_metadata.json', json.dumps(metadata, indent=2))

            # Backup all directories
            for dir_name in ['memory', 'notes', 'config', 'summaries', 'media']:
                dir_path = self.user_data / dir_name
                if dir_path.exists():
                    for file_path in dir_path.rglob('*'):
                        if file_path.is_file():
                            arcname = file_path.relative_to(self.user_data)
                            zipf.write(file_path, arcname)

        print(f"[OK] Full backup created: {backup_path}")
        return backup_path

    def create_memory_export(self, format: str = 'json') -> Path:
        """Export memories in specified format."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        if format == 'json':
            return self._export_json(timestamp)
        elif format == 'markdown':
            return self._export_markdown(timestamp)
        else:
            raise ValueError(f"Unsupported format: {format}")

    def _export_json(self, timestamp: str) -> Path:
        """Export all memories as JSON."""
        export_name = f"memories_export_{timestamp}.json"
        export_path = self.backup_dir / export_name

        # Collect all memory data
        export_data = {
            'export_date': datetime.now().isoformat(),
            'memories': {}
        }

        # Load memory files
        for memory_type in ['facts', 'preferences', 'experiences']:
            memory_file = self.user_data / "memory" / f"{memory_type}.json"
            if memory_file.exists():
                with open(memory_file, 'r', encoding='utf-8') as f:
                    export_data['memories'][memory_type] = json.load(f)

        # Load notes metadata
        notes = []
        notes_dir = self.user_data / "notes"
        if notes_dir.exists():
            for note_file in notes_dir.rglob('*.md'):
                notes.append({
                    'path': str(note_file.relative_to(self.user_data)),
                    'modified': note_file.stat().st_mtime,
                    'size': note_file.stat().st_size
                })
        export_data['notes'] = notes

        # Write export file
        with open(export_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2)

        print(f"[OK] JSON export created: {export_path}")
        return export_path

    def _export_markdown(self, timestamp: str) -> Path:
        """Export all memories as Markdown document."""
        export_name = f"memories_export_{timestamp}.md"
        export_path = self.backup_dir / export_name

        # Build markdown document
        md_lines = []
        md_lines.append(f"# 记忆导出报告")
        md_lines.append(f"\n**导出时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

        # Export facts
        md_lines.append("## 📌 事实记忆\n")
        facts_file = self.user_data / "memory" / "facts.json"
        if facts_file.exists():
            with open(facts_file, 'r', encoding='utf-8') as f:
                facts = json.load(f)
                for fact in facts.values():
                    if fact.get('status') == 'active':
                        md_lines.append(f"- **{fact.get('category', 'general')}**: {fact.get('content', '')}")
                        if fact.get('tags'):
                            md_lines.append(f"  - 标签: {', '.join(fact['tags'])}")

        # Export preferences
        md_lines.append("\n## 💝 偏好记忆\n")
        prefs_file = self.user_data / "memory" / "preferences.json"
        if prefs_file.exists():
            with open(prefs_file, 'r', encoding='utf-8') as f:
                prefs = json.load(f)
                for pref in prefs.values():
                    if pref.get('status') == 'active':
                        md_lines.append(f"- **{pref.get('category', 'general')}**: {pref.get('content', '')}")

        # Export experiences
        md_lines.append("\n## 📚 经历记忆\n")
        exp_file = self.user_data / "memory" / "experiences.json"
        if exp_file.exists():
            with open(exp_file, 'r', encoding='utf-8') as f:
                exps = json.load(f)
                for exp in exps.values():
                    if exp.get('status') == 'active':
                        date = exp.get('timestamp', '')[:10] if exp.get('timestamp') else ''
                        md_lines.append(f"- **[{date}]** {exp.get('content', '')}")

        # Notes summary
        md_lines.append("\n## 📝 笔记列表\n")
        notes_dir = self.user_data / "notes"
        if notes_dir.exists():
            for note_file in sorted(notes_dir.rglob('*.md')):
                relative_path = note_file.relative_to(notes_dir)
                md_lines.append(f"- `{relative_path}`")

        # Write markdown file
        with open(export_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(md_lines))

        print(f"[OK] Markdown export created: {export_path}")
        return export_path

    def list_backups(self) -> list:
        """List all available backups."""
        backups = []

        for backup_file in self.backup_dir.glob('backup_*.zip'):
            # Get file info
            stat = backup_file.stat()
            size_mb = stat.st_size / (1024 * 1024)

            # Try to read metadata
            metadata = {}
            try:
                with zipfile.ZipFile(backup_file, 'r') as zipf:
                    if 'backup_metadata.json' in zipf.namelist():
                        metadata = json.loads(zipf.read('backup_metadata.json'))
            except:
                pass

            backups.append({
                'filename': backup_file.name,
                'path': backup_file,
                'size_mb': round(size_mb, 2),
                'created': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                'type': metadata.get('type', 'unknown'),
                'description': metadata.get('description', '')
            })

        # Sort by creation time (newest first)
        backups.sort(key=lambda x: x['created'], reverse=True)
        return backups

    def restore_backup(self, backup_path: Path, confirm: bool = False) -> bool:
        """Restore from a backup file."""
        if not backup_path.exists():
            print(f"[!] Backup file not found: {backup_path}")
            return False

        if not confirm:
            print("[!] WARNING: This will overwrite current data!")
            response = input("Continue? (yes/no): ")
            if response.lower() != 'yes':
                print("[i] Restore cancelled")
                return False

        # Create a backup of current state first
        print("[i] Creating backup of current state...")
        self.create_full_backup("Pre-restore backup")

        # Extract backup
        print(f"[i] Restoring from: {backup_path}")
        with zipfile.ZipFile(backup_path, 'r') as zipf:
            # Skip metadata file
            files_to_extract = [f for f in zipf.namelist() if f != 'backup_metadata.json']

            for file_name in files_to_extract:
                # Extract to user-data
                target_path = self.user_data / file_name
                target_path.parent.mkdir(parents=True, exist_ok=True)

                # Extract file
                with zipf.open(file_name) as source, open(target_path, 'wb') as target:
                    target.write(source.read())

        print("[OK] Restore completed successfully")
        return True

    def auto_backup(self) -> Optional[Path]:
        """Create automatic backup if needed (daily)."""
        # Check last backup
        backups = self.list_backups()

        # Check if we need a new backup (no backup today)
        today = datetime.now().date()
        needs_backup = True

        for backup in backups:
            backup_date = datetime.fromisoformat(backup['created']).date()
            if backup_date == today:
                needs_backup = False
                break

        if needs_backup:
            return self.create_full_backup("Automatic daily backup")

        return None


def main():
    """Test backup manager."""
    import sys
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    manager = BackupManager()

    print("=== 备份管理系统 ===\n")

    while True:
        print("\n选项:")
        print("1. 创建完整备份")
        print("2. 导出记忆 (JSON)")
        print("3. 导出记忆 (Markdown)")
        print("4. 查看备份列表")
        print("5. 恢复备份")
        print("6. 退出")

        choice = input("\n请选择 (1-6): ").strip()

        if choice == '1':
            desc = input("备份描述 (可选): ").strip()
            backup_path = manager.create_full_backup(desc)
            print(f"备份已创建: {backup_path}")

        elif choice == '2':
            export_path = manager.create_memory_export('json')
            print(f"JSON导出已创建: {export_path}")

        elif choice == '3':
            export_path = manager.create_memory_export('markdown')
            print(f"Markdown导出已创建: {export_path}")

        elif choice == '4':
            backups = manager.list_backups()
            if backups:
                print("\n可用备份:")
                for i, backup in enumerate(backups[:10], 1):
                    print(f"{i}. {backup['filename']} ({backup['size_mb']}MB)")
                    print(f"   创建时间: {backup['created']}")
                    if backup['description']:
                        print(f"   描述: {backup['description']}")
            else:
                print("没有找到备份文件")

        elif choice == '5':
            backups = manager.list_backups()
            if backups:
                print("\n选择要恢复的备份:")
                for i, backup in enumerate(backups[:10], 1):
                    print(f"{i}. {backup['filename']}")

                idx = input("输入编号: ").strip()
                try:
                    idx = int(idx) - 1
                    if 0 <= idx < len(backups):
                        manager.restore_backup(backups[idx]['path'])
                    else:
                        print("无效的编号")
                except:
                    print("无效的输入")
            else:
                print("没有可恢复的备份")

        elif choice == '6':
            break

        else:
            print("无效的选择")

    print("\n再见！")


if __name__ == "__main__":
    main()