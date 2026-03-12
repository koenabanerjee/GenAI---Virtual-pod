#!/usr/bin/env python3
"""Final emoji cleanup script."""
import pathlib

# Files to clean
files_to_clean = {
    "ENHANCED_UI_README.md": [
        ('\"🎯 Custom\"', '\"Custom\"'),
    ],
    "QUICK_START_GUIDE.md": [
        ('🚀 Pipeline Progress', 'Pipeline Progress'),
        ('📝 Stories:', 'Stories:'),
        ('💻 Code:', 'Code:'),
        ('🏗️ Designs:', 'Designs:'),
        ('🧪 Tests:', 'Tests:'),
        ('🎨 UI Pages:', 'UI Pages:'),
        ('📝 analysis', 'analysis'),
        ('✅ completed', 'completed'),
        ('🎨 ui_design', 'ui_design'),
        ('🏗️ design', 'design'),
        ('💻 development', 'development'),
        ('🧪 testing', 'testing'),
    ],
}

for filepath, replacements in files_to_clean.items():
    try:
        file_path = pathlib.Path(filepath)
        if not file_path.exists():
            print(f"File {filepath} not found")
            continue
        
        content = file_path.read_text(encoding='utf-8')
        original = content
        
        for old, new in replacements:
            content = content.replace(old, new)
        
        if content != original:
            file_path.write_text(content, encoding='utf-8')
            print(f"✓ Cleaned {filepath}")
        else:
            print(f"- No emojis found in {filepath}")
    except Exception as e:
        print(f"✗ Error processing {filepath}: {e}")

print("\nCleanup complete!")
