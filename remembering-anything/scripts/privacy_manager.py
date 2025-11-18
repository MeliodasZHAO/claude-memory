#!/usr/bin/env python3
"""
Privacy Manager - Handle sensitive information with encryption and access control.

Features:
- Simple encryption for sensitive memories
- Privacy levels (public, private, sensitive)
- Password protection for sensitive data
"""

import json
import hashlib
import base64
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime


class PrivacyManager:
    """Manage privacy and encryption for memories."""

    PRIVACY_LEVELS = {
        'public': 0,      # Can be freely accessed and shared
        'private': 1,     # Only shown when explicitly asked
        'sensitive': 2    # Requires password/confirmation
    }

    def __init__(self, password: Optional[str] = None):
        """Initialize privacy manager."""
        self.skill_dir = Path(__file__).parent.parent
        self.user_data = self.skill_dir / "user-data"
        self.config_file = self.user_data / "config" / "privacy_config.json"

        # Load or create privacy config
        self.config = self._load_config()

        # Set master password (simplified encryption)
        self.password = password or self.config.get('default_password', 'default_key_123')

    def _load_config(self) -> dict:
        """Load privacy configuration."""
        if self.config_file.exists():
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            'encryption_enabled': False,
            'default_privacy_level': 'public',
            'sensitive_keywords': ['密码', 'password', '银行', 'bank', 'secret', '秘密'],
            'auto_encrypt_sensitive': True
        }

    def _save_config(self):
        """Save privacy configuration."""
        self.config_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=2)

    def simple_encrypt(self, text: str) -> str:
        """Simple XOR encryption (not secure, but good enough for basic privacy)."""
        # Create a key from password
        key = hashlib.sha256(self.password.encode()).digest()

        # XOR each character with key
        encrypted = []
        for i, char in enumerate(text):
            key_char = key[i % len(key)]
            encrypted_char = chr(ord(char) ^ key_char)
            encrypted.append(encrypted_char)

        # Encode to base64 for storage
        encrypted_str = ''.join(encrypted)
        return base64.b64encode(encrypted_str.encode('utf-8', errors='ignore')).decode('ascii')

    def simple_decrypt(self, encrypted_text: str) -> str:
        """Decrypt text encrypted with simple_encrypt."""
        try:
            # Decode from base64
            encrypted_str = base64.b64decode(encrypted_text).decode('utf-8', errors='ignore')

            # Create same key from password
            key = hashlib.sha256(self.password.encode()).digest()

            # XOR each character with key (XOR is reversible)
            decrypted = []
            for i, char in enumerate(encrypted_str):
                key_char = key[i % len(key)]
                decrypted_char = chr(ord(char) ^ key_char)
                decrypted.append(decrypted_char)

            return ''.join(decrypted)
        except Exception as e:
            return f"[解密失败: {str(e)}]"

    def detect_privacy_level(self, content: str) -> str:
        """Auto-detect privacy level based on content."""
        content_lower = content.lower()

        # Check for sensitive keywords
        for keyword in self.config['sensitive_keywords']:
            if keyword in content_lower:
                return 'sensitive'

        # Check for private indicators
        private_indicators = ['个人', 'personal', '私人', 'private']
        for indicator in private_indicators:
            if indicator in content_lower:
                return 'private'

        return 'public'

    def process_memory(self, memory: Dict[str, Any]) -> Dict[str, Any]:
        """Process a memory with privacy settings."""
        content = memory.get('content', '')

        # Auto-detect privacy level if not set
        if 'privacy_level' not in memory:
            memory['privacy_level'] = self.detect_privacy_level(content)

        # Encrypt if sensitive and auto-encrypt is enabled
        if memory['privacy_level'] == 'sensitive' and self.config['auto_encrypt_sensitive']:
            if not memory.get('encrypted', False):
                memory['content_encrypted'] = self.simple_encrypt(content)
                memory['content'] = '[已加密内容]'
                memory['encrypted'] = True
                memory['encryption_time'] = datetime.now().isoformat()

        return memory

    def decrypt_memory(self, memory: Dict[str, Any], password: Optional[str] = None) -> Dict[str, Any]:
        """Decrypt an encrypted memory."""
        if not memory.get('encrypted', False):
            return memory

        # Use provided password or default
        if password:
            old_password = self.password
            self.password = password

        # Decrypt
        decrypted_memory = memory.copy()
        if 'content_encrypted' in memory:
            decrypted_memory['content'] = self.simple_decrypt(memory['content_encrypted'])
            decrypted_memory['decrypted'] = True

        # Restore password
        if password:
            self.password = old_password

        return decrypted_memory

    def filter_memories_by_privacy(self, memories: Dict[str, Dict],
                                  include_private: bool = False,
                                  include_sensitive: bool = False) -> Dict[str, Dict]:
        """Filter memories based on privacy level."""
        filtered = {}

        for mem_id, memory in memories.items():
            privacy_level = memory.get('privacy_level', 'public')

            if privacy_level == 'public':
                filtered[mem_id] = memory
            elif privacy_level == 'private' and include_private:
                filtered[mem_id] = memory
            elif privacy_level == 'sensitive' and include_sensitive:
                # Return encrypted version unless explicitly decrypted
                filtered[mem_id] = memory

        return filtered

    def set_privacy_level(self, memory_id: str, level: str, memory_type: str = 'facts'):
        """Set privacy level for a specific memory."""
        # Load the memory file
        memory_file = self.user_data / "memory" / f"{memory_type}.json"
        if not memory_file.exists():
            print(f"Memory file not found: {memory_file}")
            return False

        with open(memory_file, 'r', encoding='utf-8') as f:
            memories = json.load(f)

        if memory_id not in memories:
            print(f"Memory not found: {memory_id}")
            return False

        # Update privacy level
        memories[memory_id]['privacy_level'] = level
        memories[memory_id]['privacy_updated'] = datetime.now().isoformat()

        # Process with new privacy level
        memories[memory_id] = self.process_memory(memories[memory_id])

        # Save back
        with open(memory_file, 'w', encoding='utf-8') as f:
            json.dump(memories, f, ensure_ascii=False, indent=2)

        return True

    def create_privacy_report(self) -> str:
        """Generate a report of all private/sensitive memories."""
        report = []
        report.append("=== 隐私记忆报告 ===\n")

        # Check all memory types
        for memory_type in ['facts', 'preferences', 'experiences']:
            memory_file = self.user_data / "memory" / f"{memory_type}.json"
            if not memory_file.exists():
                continue

            with open(memory_file, 'r', encoding='utf-8') as f:
                memories = json.load(f)

            private_count = 0
            sensitive_count = 0
            encrypted_count = 0

            for memory in memories.values():
                level = memory.get('privacy_level', 'public')
                if level == 'private':
                    private_count += 1
                elif level == 'sensitive':
                    sensitive_count += 1
                if memory.get('encrypted', False):
                    encrypted_count += 1

            if private_count or sensitive_count or encrypted_count:
                report.append(f"\n{memory_type.capitalize()}:")
                report.append(f"  - 私密记忆: {private_count}")
                report.append(f"  - 敏感记忆: {sensitive_count}")
                report.append(f"  - 已加密: {encrypted_count}")

        return '\n'.join(report)


def main():
    """Test privacy manager."""
    import sys
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    manager = PrivacyManager()

    print("=== 隐私管理系统测试 ===\n")

    # Test encryption
    print("1. 测试加密功能:")
    test_text = "这是我的银行密码提示：生日+1234"
    print(f"原文: {test_text}")

    encrypted = manager.simple_encrypt(test_text)
    print(f"加密后: {encrypted[:50]}...")

    decrypted = manager.simple_decrypt(encrypted)
    print(f"解密后: {decrypted}")

    # Test privacy detection
    print("\n2. 测试隐私级别检测:")
    test_cases = [
        "今天天气真好",
        "我的个人邮箱是xxx@gmail.com",
        "银行卡密码是123456"
    ]

    for text in test_cases:
        level = manager.detect_privacy_level(text)
        print(f"  '{text[:20]}...' -> {level}")

    # Test memory processing
    print("\n3. 测试记忆处理:")
    test_memory = {
        'id': 'test_001',
        'content': '信用卡密码提示：anniversary',
        'type': 'fact'
    }

    processed = manager.process_memory(test_memory.copy())
    print(f"  处理前: {test_memory['content']}")
    print(f"  处理后: {processed['content']}")
    print(f"  加密状态: {processed.get('encrypted', False)}")

    # Generate report
    print("\n4. 隐私报告:")
    print(manager.create_privacy_report())


if __name__ == "__main__":
    main()