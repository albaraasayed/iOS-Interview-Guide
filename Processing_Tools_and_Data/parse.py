import json
import re

def parse_markdown(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    questions = []
    current_q = None
    current_a = []

    # regex to match a question header: #, ##, ###, #### followed by text that looks like a question or concept
    # Actually, let's just look for headers that end with '?' or seem to be questions.
    header_pattern = re.compile(r'^(#{1,6})\s+(.*)$')
    
    for line in lines:
        match = header_pattern.match(line)
        if match:
            level = len(match.group(1))
            text = match.group(2).strip()
            # In an interview doc, usually questions are headers
            # We skip Table of Contents, Practice, etc.
            if text.lower() in ["hello fellow ios developers!", "what is this for?", "practice", "table of contents", "interview questions & answers", "contributing", "thank you", "flashcards", "database", "debugging", "design patterns", "general / uncategorized", "memory management", "networking", "objective-c", "swift", "thread management", "unit testing / ui testing", "view / storyboard", "algorithm resources"]:
                continue
                
            # If we had an active question, save it
            if current_q:
                questions.append({
                    "question": current_q,
                    "answer": "".join(current_a).strip()
                })
            current_q = text
            current_a = []
        else:
            if current_q:
                current_a.append(line)
                
    if current_q:
        questions.append({
            "question": current_q,
            "answer": "".join(current_a).strip()
        })

    with open('parsed_questions.json', 'w', encoding='utf-8') as f:
        json.dump(questions, f, indent=2)

    print(f"Extracted {len(questions)} questions.")

if __name__ == "__main__":
    parse_markdown('/Users/moca/Documents/Coding/iOS Interview Questions/README.md')
