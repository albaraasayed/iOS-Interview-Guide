import json
import re
from collections import defaultdict

with open('parsed_questions.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)

categories = {
    "Objective-C": ["objective-c", "ns", "swizzle", "dynamic", "synthesize", "category", "extension"],
    "Swift Fundamentals": ["swift", "var", "let", "struct", "class", "protocol", "delegate", "closure", "optional", "guard", "defer", "inout", "lazy", "mutating", "escaping", "autoclosure"],
    "Reactive Programming": ["rxswift", "combine", "publisher", "subscriber", "observable", "subject"],
    "Design Patterns & Architecture": ["mvc", "mvvm", "viper", "singleton", "pattern", "solid", "oop", "architecture", "dependency injection", "factory", "coordinator"],
    "Core Data & Persistence": ["core data", "coredata", "nsuserdefault", "userdefaults", "keychain", "sqlite", "realm", "persistence", "managed object"],
    "SwiftUI": ["swiftui", "state", "binding", "environmentobject", "observedobject", "published", "viewbuilder"],
    "SwiftData": ["swiftdata", "model", "modelcontext", "modelcontainer"],
    "Third-Party Libraries & Dependency Management": ["cocoapods", "carthage", "spm", "swift package manager", "alamofire", "kingfisher", "dependency management"],
    "General Computer Science, OS & Multithreading": ["gcd", "multithreading", "thread", "concurrency", "operation", "operationqueue", "memory", "arc", "retain cycle", "weak", "unowned", "strong", "deadlock", "race condition", "heap", "stack", "algorithm", "big o", "data structure"],
    "UIKit": ["uikit", "uiview", "uiviewcontroller", "uitableview", "uicollectionview", "autolayout", "storyboard", "xib", "frame", "bounds", "intrinsic", "responder"],
    "iOS Fundamentals": ["ios", "app delegate", "scenedelegate", "lifecycle", "background", "foreground", "push notification", "plist", "info.plist", "certificate", "provisioning", "app store"]
}

clustered = defaultdict(list)

for q in questions:
    q_text = q['question'].lower()
    assigned = False
    
    # Try to assign based on question text first
    for cat, keywords in categories.items():
        if any(kw in q_text for kw in keywords):
            clustered[cat].append(q)
            assigned = True
            break
            
    # If not assigned, try answer text
    if not assigned:
        a_text = q['answer'].lower()
        for cat, keywords in categories.items():
            if any(kw in a_text for kw in keywords):
                clustered[cat].append(q)
                assigned = True
                break
                
    if not assigned:
        clustered["Misc"].append(q)

for cat, qs in clustered.items():
    print(f"{cat}: {len(qs)} questions")
    
with open('clustered_questions.json', 'w', encoding='utf-8') as f:
    json.dump(clustered, f, indent=2)
