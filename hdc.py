import os
import pickle
import numpy as np
from collections import defaultdict
from tqdm import tqdm

trigram_vector_file = 'models/space_trigram_vectors.pkl'
language_vector_file = 'models/space_language_vectors.pkl'

def load_vectors(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            return pickle.load(f)
    else:
        print(f"Warning: {file_path} not found.")
        return None

def generate_trigram_vectors(trigram_dir):
    trigram_vectors = {}

    for root, _, files in os.walk(trigram_dir):
        for file in tqdm(files):
            if file.endswith('.txt'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        trigram = line.strip()
                        if trigram not in trigram_vectors:
                            trigram_vectors[trigram] = np.random.choice([-1, 1], size=10000)

    with open(trigram_vector_file, 'wb') as f:
        pickle.dump(trigram_vectors, f)

    print("Trigram vectors saved.")

def compute_language_vectors(trigram_dir, language_vector_file='language_vectors.pkl'):
    trigram_vectors = load_vectors(trigram_vector_file)
    if trigram_vectors is None:
        return

    language_vectors = defaultdict(lambda: np.zeros(10000))
    file_count = 0

    with open(language_vector_file, 'wb') as f:
        pickle.dump({}, f)
        f.flush()
        os.fsync(f.fileno())

    for root, _, files in os.walk(trigram_dir):
        for file in tqdm(files, desc=f"Processing {root}"):
            if file.endswith('.txt'):
                language = os.path.basename(root)
                file_path = os.path.join(root, file)

                with open(file_path, 'r', encoding='utf-8') as f:
                    lines_processed = 0
                    for line in f:
                        trigram = line.strip()
                        if trigram in trigram_vectors:
                            language_vectors[language] += trigram_vectors[trigram]
                            lines_processed += 1
                file_count += 1

            if file_count % 10 == 0:
                with open(language_vector_file, 'wb') as f:
                    pickle.dump(dict(language_vectors), f)
                    f.flush()
                    os.fsync(f.fileno())

    for language in language_vectors:
        norm = np.linalg.norm(language_vectors[language])
        if norm != 0:
            language_vectors[language] /= norm
        else:
            print(f"Warning: Zero vector for language {language}, cannot normalize.")

    with open(language_vector_file, 'wb') as f:
        pickle.dump(dict(language_vectors), f)
        f.flush()
        os.fsync(f.fileno())

    print("Final language vectors saved. Number of languages:", len(language_vectors))

def generate_trigrams(text):
    text = text.lower().replace('\n', ' ').replace('\r', ' ')
    return [text[i:i+3] for i in range(len(text) - 2)]

def cosine_similarity(vec1, vec2):
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

def detect_language(test_text):
    trigram_vectors = load_vectors(trigram_vector_file)
    language_vectors = load_vectors(language_vector_file)

    test_trigrams = generate_trigrams(test_text)
    test_vector = np.zeros(10000)

    for trigram in test_trigrams:
        if trigram in trigram_vectors:
            test_vector += trigram_vectors[trigram]
    
    test_vector /= np.linalg.norm(test_vector)

    best_language = None
    best_similarity = -1

    for language, vector in language_vectors.items():
        similarity = cosine_similarity(test_vector, vector)
        if similarity > best_similarity:
            best_similarity = similarity
            best_language = language

    return best_language, best_similarity