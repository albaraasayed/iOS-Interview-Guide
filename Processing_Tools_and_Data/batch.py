import json
import math
import os
import re
from collections import Counter, defaultdict

# Simple TF-IDF and Cosine Similarity in pure Python
def get_words(text):
    return re.findall(r'\w+', text.lower())

def tf(word_counts):
    total = sum(word_counts.values())
    return {word: count / total for word, count in word_counts.items()} if total > 0 else {}

def compute_idf(documents):
    n = len(documents)
    idf = defaultdict(float)
    for doc in documents:
        for word in set(doc.keys()):
            idf[word] += 1
    return {word: math.log(n / count) for word, count in idf.items()}

def tf_idf(tf_dict, idf_dict):
    return {word: tf_val * idf_dict.get(word, 0) for word, tf_val in tf_dict.items()}

def cosine_similarity(vec1, vec2):
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])
    sum1 = sum([vec1[x]**2 for x in vec1.keys()])
    sum2 = sum([vec2[x]**2 for x in vec2.keys()])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)
    if not denominator:
        return 0.0
    return float(numerator) / denominator

def main():
    with open('parsed_questions.json', 'r', encoding='utf-8') as f:
        questions = json.load(f)

    # Prepare documents (using both question and a bit of answer for better similarity)
    docs = [Counter(get_words(q['question'] + " " + q['answer'][:200])) for q in questions]
    idf = compute_idf(docs)
    tfidf_docs = [tf_idf(tf(doc), idf) for doc in docs]

    # Simple agglomerative clustering
    n = len(questions)
    clusters = {i: [i] for i in range(n)}
    cluster_mapping = {i: i for i in range(n)}

    print("Computing similarities and clustering...")
    for i in range(n):
        for j in range(i + 1, n):
            sim = cosine_similarity(tfidf_docs[i], tfidf_docs[j])
            if sim > 0.4: # Similarity threshold for potential duplicates
                ci = cluster_mapping[i]
                cj = cluster_mapping[j]
                if ci != cj:
                    # Merge ci and cj
                    clusters[ci].extend(clusters[cj])
                    for item in clusters[cj]:
                        cluster_mapping[item] = ci
                    del clusters[cj]

    # Create batches of max size ~25
    batches = []
    current_batch = []
    
    for c_id, item_indices in clusters.items():
        cluster_items = [questions[idx] for idx in item_indices]
        if len(current_batch) + len(cluster_items) > 25 and len(current_batch) > 0:
            batches.append(current_batch)
            current_batch = []
        current_batch.extend(cluster_items)
    
    if current_batch:
        batches.append(current_batch)

    print(f"Total questions: {n}")
    print(f"Total clusters: {len(clusters)}")
    print(f"Total batches created: {len(batches)}")

    os.makedirs('batches', exist_ok=True)
    for i, batch in enumerate(batches):
        with open(f'batches/batch_{i}.json', 'w', encoding='utf-8') as f:
            json.dump(batch, f, indent=2)

if __name__ == "__main__":
    main()
