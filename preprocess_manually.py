import sys
import os
import re
from bs4 import BeautifulSoup
from tqdm import tqdm
import nltk

nltk_data_dir = os.path.join(os.getcwd(), "nltk_data")
nltk.data.path.append(nltk_data_dir)

punkt_path = os.path.join(nltk_data_dir, "tokenizers", "punkt")
if not os.path.exists(punkt_path):
    with open(os.devnull, 'w') as f:
        old_stdout = sys.stdout
        sys.stdout = f
        try:
            nltk.download("punkt", download_dir=nltk_data_dir)
        finally:
            sys.stdout = old_stdout

ENGLISH_ABBREVIATIONS = {
    "p.m.", "a.m.", "dr.", "mr.", "mrs.", "u.s.a.", "e.g.", "i.e.", "etc.", "vs.", "fig.", "vol.", "no.", "pp."
}

ITALIAN_ABBREVIATIONS = {
    "p.m.", "a.m.", "dott.", "sig.", "e.g.", "i.e.", "etc.", "vs.", "fig.", "vol.", "art.", "avv.", "prof.", "ing.",
    "arch.", "geom.", "rag.", "dott.ssa", "sig.ra", "sig.na", "dott.ri", "sig.ri", "sig.re", "dott.sse", "sig.re"
}

GERMAN_ABBREVIATIONS = {
    "p.m.", "a.m.", "d.h.", "z.B.", "u.a.", "etc.", "vgl.", "usw.", "bzw.", "ff.", "u.E.", "g.U.", "g.g.A.", "c.-à-d",
    "Buchst.", "u.s.w.", "sog.", "u.ä.", "Std.", "evtl.", "Zt.", "Chr.", "u.U.", "o.ä.", "Ltd.", "b.A.", "z.Zt.", "spp.",
    "sen.", "SA", "k.o.", "jun.", "i.H.v.", "dgl.", "dergl.", "Co.", "zzt.", "usf.", "s.p.a.", "Dkr.", "Corp.", "bzgl.", "BSE"
}

def de_xml_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
    except UnicodeDecodeError:
        try:
            with open(file_path, 'r', encoding='latin-1') as file:
                content = file.read()
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return None
    
    soup = BeautifulSoup(content, "html.parser")
    text = soup.get_text()
    return text

def preprocess_text(text, language):
    text = text.lower()

    if language == "en":
        abbreviations = ENGLISH_ABBREVIATIONS
    elif language == "it":
        abbreviations = ITALIAN_ABBREVIATIONS
    elif language == "de":
        abbreviations = GERMAN_ABBREVIATIONS
    else:
        abbreviations = set()

    for abbr in abbreviations:
        text = text.replace(abbr, abbr.replace(".", "_"))

    text = re.sub(r"[^a-z ]", "", text)
    text = re.sub(r"\s+", " ", text)
    text = text.replace("_", ".")

    return text

def extract_trigrams(text):
    trigrams = []
    for i in range(len(text) - 2):
        trigram = text[i:i+3]
        if trigram.replace(" ", "").isalpha():
            trigrams.append(trigram)
    return trigrams

def process_file(file_path, language):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    sentences = nltk.tokenize.sent_tokenize(text)

    trigrams = []
    for sentence in sentences:
        preprocessed = preprocess_text(sentence, language)
        trigrams.extend(extract_trigrams(preprocessed))

    return trigrams

def process_dir_manually(input_dir, output_dir, language):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for root, _, files in os.walk(input_dir):
        for file in tqdm(files, desc=f"Processing {root}"):
            if file.endswith('.txt'):
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(root, input_dir)
                output_subdir = os.path.join(output_dir, relative_path)
                
                if not os.path.exists(output_subdir):
                    os.makedirs(output_subdir)
                
                output_file_path = os.path.join(output_subdir, file)
                trigrams = process_file(file_path, language)
                
                if trigrams:
                    with open(output_file_path, 'w', encoding='utf-8') as output_file:
                        for trigram in trigrams:
                            output_file.write(trigram + '\n')