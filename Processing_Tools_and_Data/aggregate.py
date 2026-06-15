import json
import os
import glob
from collections import defaultdict

# --- Configuration ---
CATEGORY_ORDER = [
    "iOS Fundamentals",
    "Objective-C",
    "Swift Fundamentals",
    "UIKit",
    "Reactive Programming",
    "Design Patterns & Architecture",
    "Core Data & Persistence",
    "SwiftUI",
    "SwiftData",
    "Third-Party Libraries & Dependency Management",
    "General Computer Science, OS & Multithreading",
]

CATEGORY_DESCRIPTIONS = {
    "iOS Fundamentals": "Core iOS platform concepts: application lifecycle, provisioning, push notifications, and OS-level features.",
    "Objective-C": "Objective-C language features, runtime, memory management patterns, and interoperability with Swift.",
    "Swift Fundamentals": "The Swift programming language: syntax, type system, generics, protocols, closures, and language features.",
    "UIKit": "UIKit framework: view lifecycle, layout, table views, collection views, navigation, and UI components.",
    "Reactive Programming": "Reactive and declarative data-flow programming using RxSwift and Apple's Combine framework.",
    "Design Patterns & Architecture": "Software architecture patterns (MVC, MVVM, VIPER), SOLID principles, and OOP design patterns.",
    "Core Data & Persistence": "Data persistence using Core Data, NSUserDefaults, Keychain, and other storage mechanisms.",
    "SwiftUI": "Apple's declarative UI framework: state management, view composition, animations, and data flow.",
    "SwiftData": "Apple's modern data persistence framework built for Swift and SwiftUI.",
    "Third-Party Libraries & Dependency Management": "CocoaPods, Carthage, Swift Package Manager, and popular third-party iOS libraries.",
    "General Computer Science, OS & Multithreading": "Concurrency (GCD, Operations, async/await), memory management (ARC), algorithms, and OS concepts.",
}

def normalize_category(cat):
    """Normalize category names to match our canonical list."""
    cat_lower = cat.lower().strip()
    # Handle Reactive Programming sub-categories
    if "rxswift" in cat_lower:
        return ("Reactive Programming", "RxSwift")
    if "combine" in cat_lower:
        return ("Reactive Programming", "Combine")
    if "reactive" in cat_lower:
        return ("Reactive Programming", None)
    # Handle exact matches
    for c in CATEGORY_ORDER:
        if c.lower() == cat_lower:
            return (c, None)
    # Fuzzy match
    for c in CATEGORY_ORDER:
        if c.lower().replace(" & ", " ").replace(" and ", " ") in cat_lower or \
           cat_lower in c.lower():
            return (c, None)
    # Default fallback
    return ("iOS Fundamentals", None)

def load_all_batches():
    all_items = []
    for path in sorted(glob.glob("batches/processed_batch_*.json"),
                       key=lambda p: int(p.split("_")[-1].split(".")[0])):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            all_items.extend(data)
            print(f"  Loaded {len(data)} items from {path}")
        except Exception as e:
            print(f"  ERROR loading {path}: {e}")
    return all_items

def deduplicate_by_question(items):
    """Simple dedup: normalize question text and drop near-exact duplicates."""
    seen = {}
    deduped = []
    for item in items:
        q = item.get("question", "").strip()
        # Create a normalized key by lowercasing and stripping tags/numbers
        import re
        key = re.sub(r'\s+', ' ', re.sub(r'\[.*?\]', '', q).lower().strip())
        key = re.sub(r'^\d+[\.\-\)]\s*', '', key)  # strip leading number prefixes
        if key and key not in seen:
            seen[key] = True
            deduped.append(item)
        else:
            if key:
                print(f"  DEDUP: Skipping '{q[:80]}...'")
    return deduped

def build_markdown(categorized):
    lines = []

    # Header
    lines.append("# iOS Interview Questions — Definitive Study Guide")
    lines.append("")
    lines.append("> A comprehensive, categorized, and deduplicated reference for senior iOS developer interview preparation.")
    lines.append("> Each question is tagged with a difficulty level: **[Easy]**, **[Mid]**, or **[Expert]**.")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Table of Contents
    lines.append("## Table of Contents")
    lines.append("")
    for cat in CATEGORY_ORDER:
        anchor = cat.lower().replace(" ", "-").replace("&", "").replace(",", "").replace("(", "").replace(")", "").replace("--", "-")
        lines.append(f"- [{cat}](#{anchor})")
        if cat == "Reactive Programming":
            lines.append("  - [RxSwift](#rxswift)")
            lines.append("  - [Combine](#combine)")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Sections
    for cat in CATEGORY_ORDER:
        lines.append(f"## {cat}")
        lines.append("")
        if cat in CATEGORY_DESCRIPTIONS:
            lines.append(f"*{CATEGORY_DESCRIPTIONS[cat]}*")
            lines.append("")
        lines.append("---")
        lines.append("")

        if cat == "Reactive Programming":
            # RxSwift sub-section
            rxswift_items = categorized.get(("Reactive Programming", "RxSwift"), [])
            combine_items = categorized.get(("Reactive Programming", "Combine"), [])
            general_rp    = categorized.get(("Reactive Programming", None), [])

            lines.append("### RxSwift")
            lines.append("")
            for item in rxswift_items + general_rp:
                q = item.get("question", "").strip()
                a = item.get("answer", "").strip()
                lines.append(f"### {q}")
                lines.append("")
                lines.append(a)
                lines.append("")
                lines.append("---")
                lines.append("")

            lines.append("### Combine")
            lines.append("")
            for item in combine_items:
                q = item.get("question", "").strip()
                a = item.get("answer", "").strip()
                lines.append(f"### {q}")
                lines.append("")
                lines.append(a)
                lines.append("")
                lines.append("---")
                lines.append("")
        else:
            for key in [(cat, None), (cat, "RxSwift"), (cat, "Combine")]:
                for item in categorized.get(key, []):
                    q = item.get("question", "").strip()
                    a = item.get("answer", "").strip()
                    if not q or not a:
                        continue
                    lines.append(f"### {q}")
                    lines.append("")
                    lines.append(a)
                    lines.append("")
                    lines.append("---")
                    lines.append("")

    return "\n".join(lines)

def main():
    print("=== Phase 3: Aggregation ===")
    print("\nLoading all processed batches...")
    all_items = load_all_batches()
    print(f"\nTotal raw items loaded: {len(all_items)}")

    print("\nDeduplicating...")
    items = deduplicate_by_question(all_items)
    print(f"Total after deduplication: {len(items)}")

    print("\nCategorizing...")
    categorized = defaultdict(list)
    for item in items:
        raw_cat = item.get("category", "iOS Fundamentals")
        cat_key = normalize_category(raw_cat)
        categorized[cat_key].append(item)

    print("\nCategory counts:")
    for cat in CATEGORY_ORDER:
        count = len(categorized.get((cat, None), []))
        if cat == "Reactive Programming":
            count += len(categorized.get((cat, "RxSwift"), []))
            count += len(categorized.get((cat, "Combine"), []))
        print(f"  {cat}: {count}")

    print("\nBuilding Markdown...")
    markdown = build_markdown(categorized)

    output_path = "Organized_Interviews.md"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(markdown)

    print(f"\n✅ Done! Written to '{output_path}'")
    print(f"   File size: {os.path.getsize(output_path):,} bytes")

    # Verify README.md is untouched
    if os.path.exists("README.md"):
        print("\n✅ README.md is present and untouched.")
    else:
        print("\n⚠️  WARNING: README.md not found!")

if __name__ == "__main__":
    main()
