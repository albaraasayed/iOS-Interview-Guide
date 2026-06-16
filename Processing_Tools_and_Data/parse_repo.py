import re
import json

def analyze_readme():
    with open('README.md', 'r') as f:
        content = f.read()
    
    headers = re.findall(r'^#+\s+(.*)$', content, re.MULTILINE)
    return headers

print(json.dumps(analyze_readme(), indent=2))
