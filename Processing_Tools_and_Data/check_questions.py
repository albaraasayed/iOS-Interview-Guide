import re
import json

with open('README.md', 'r') as f:
    content = f.read().lower()

questions_to_check = [
    "Completion Handler vs Task",
    "@autoclosure",
    "Variadic Functions",
    "Advanced Set Operations",
    "Cocoa vs. Cocoa Touch",
    "SpriteKit and SceneKit",
    "UI Automation API",
    "Legacy JSON Frameworks",
    "Linux/General Software Design",
    "Algorithm Resources",
    "waterfall methodology and Agile methodology",
    "difference between a class and an object",
    "What is JSON? What are the pros and cons",
    "JSON framework supported by iOS",
    "What is a Factory",
    "What is an Observer",
    "What is a Coordinator",
    "What is a Proxy",
    "What is Codable",
    "Do enums have strong or weak references",
    "first method that gets called in iOS",
    "how is the main UIWindow instantiated",
    "Recursive enumeration",
    "List two types of classes in Swift",
    "identify the layout of elements in UIView",
    "@synchronized",
    "What is UIApplication",
    "changes in UserNotifications",
    "Dedicated Definitions: Standalone, deep-dive explanations defining @State and @StateObject"
]

results = {}
for q in questions_to_check:
    results[q] = q.lower() in content

print(json.dumps(results, indent=2))
