import os
import pickle
import numpy as np
from collections import defaultdict
from tqdm import tqdm

trigram_vector_file = 'trigram_vectors.pkl'
language_profile_file='language_profiles.pkl'

def generate_trigram_vectors(trigram_dir):
    trigram_vectors = {}
    for root, dirs, files in os.walk(trigram_dir):
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

    print(f"Trigram vectors saved")

def compute_language_profiles(trigram_dir):
    with open(trigram_vector_file, 'rb') as f:
        trigram_vectors = pickle.load(f)

    language_profiles = defaultdict(lambda: np.zeros(10000))

    for root, dirs, files in os.walk(trigram_dir):
        for file in tqdm(files, desc=f"Processing {root}"):
            if file.endswith('.txt'):
                language = os.path.basename(root)
                file_path = os.path.join(root, file)
                
                with open(file_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        trigram = line.strip()
                        if trigram in trigram_vectors:
                            language_profiles[language] += trigram_vectors[trigram]
    
    for language in language_profiles:
        language_profiles[language] /= np.linalg.norm(language_profiles[language])

    with open(profile_file, 'wb') as f:
        pickle.dump(language_profiles, f)
    
    print(f"Language profiles saved to {profile_file}")
    return language_profiles
