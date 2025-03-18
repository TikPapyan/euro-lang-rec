import os
from bs4 import BeautifulSoup
from tqdm import tqdm
import nltk

nltk_data_dir = os.path.join(os.getcwd(), "nltk_data")
nltk.data.path.append(nltk_data_dir)

punkt_path = os.path.join(nltk_data_dir, "tokenizers", "punkt")
if not os.path.exists(punkt_path):
    nltk.download("punkt_tab", download_dir=nltk_data_dir)

def de_xml_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
    except UnicodeDecodeError:
        try:
            with open(file_path, 'r', encoding='latin-1') as file:
                content = file.read()
        except Exception as e:
            logging.error(f"Error reading {file_path}: {e}")
            return None
    
    soup = BeautifulSoup(content, "html.parser")
    text = soup.get_text()
    return text

def de_xml_dir(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for root, dirs, files in os.walk(input_dir):
        for file in tqdm(files):
            if file.endswith('.txt'):
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(root, input_dir)
                output_subdir = os.path.join(output_dir, relative_path)
                
                if not os.path.exists(output_subdir):
                    os.makedirs(output_subdir)
                
                output_file_path = os.path.join(output_subdir, file)
                text = de_xml_file(file_path)
                
                if text:
                    with open(output_file_path, 'w', encoding='utf-8') as output_file:
                        output_file.write(text)

def generate_trigrams(text):
    text = text.lower().replace('\n', ' ').replace('\r', ' ')
    return [text[i:i+3] for i in range(len(text) - 2)]

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    
    sentences = nltk.tokenize.sent_tokenize(text)
    trigrams = []
    for sentence in sentences:
        if len(sentence) >= 3:
            trigrams.extend(generate_trigrams(sentence))
    return trigrams

def process_dir(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for root, dirs, files in os.walk(input_dir):
        for file in tqdm(files):
            if file.endswith('.txt'):
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(root, input_dir)
                output_subdir = os.path.join(output_dir, relative_path)
                
                if not os.path.exists(output_subdir):
                    os.makedirs(output_subdir)
                
                output_file_path = os.path.join(output_subdir, file)
                trigrams = process_file(file_path)
                
                if trigrams:
                    with open(output_file_path, 'w', encoding='utf-8') as output_file:
                        for trigram in trigrams:
                            output_file.write(trigram + '\n')