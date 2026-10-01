import os

PROJECT_DIR = r"C:\Users\rodri\.gemini\antigravity\scratch\renting_project"
base_path = os.path.join(PROJECT_DIR, 'templates', 'base.html')

with open(base_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace whatever the title is currently with the proper unicode one
import re
content = re.sub(r'<title>.*?</title>', '<title>\U0001f69c Renta Testa</title>', content)

with open(base_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Title fixed with proper emoji")
