import re
from pathlib import Path

# regex matching most emoji codepoints
emoji_pattern = re.compile(
    "[" 
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F600-\U0001F64F"  # emoticons
    "\U0001F680-\U0001F6FF"  # transport & map
    "\U0001F700-\U0001F77F"  # alchemical symbols
    "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
    "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
    "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
    "\U0001FA00-\U0001FA6F"  # Chess Symbols etc.
    "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
    "\U00002700-\U000027BF"  # Dingbats
    "\U00002600-\U000026FF"  # Miscellaneous Symbols
    "]+",
    flags=re.UNICODE,
)

for path in Path('.').rglob('*.md'):
    text = path.read_text(encoding='utf-8')
    new = emoji_pattern.sub('', text)
    if new != text:
        path.write_text(new, encoding='utf-8')
        print(f"cleaned {path}")
