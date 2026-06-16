import re

with open('index.html', 'r') as f:
    html = f.read()

sections = re.findall(r'<section\s+id="([^"]+)".*?>\s*<div\s+class="category-header">\s*<h2[^>]*>(.*?)</h2>', html, re.DOTALL | re.IGNORECASE)
for s in sections:
    print(f"ID: {s[0]} - Title: {s[1]}")
