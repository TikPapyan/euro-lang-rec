import os

from preprocess import de_xml_dir, process_dir
from hdc import generate_trigram_vectors, compute_language_vectors, detect_language
from preprocess_manually import process_dir_manually

input_dir = 'txt'
output_dir = 'de_xml_txt'
trigram_dir = 'trigrams/with_spaces'

def main():
    # print("De-XMLing files...")
    # de_xml_dir(input_dir, output_dir)

    # process_dir_manually(os.path.join(output_dir, "en"), os.path.join(trigram_dir, "en"), language="en")
    # process_dir_manually(os.path.join(output_dir, "it"), os.path.join(trigram_dir, "it"), language="it")
    # process_dir_manually(os.path.join(output_dir, "de"), os.path.join(trigram_dir, "de"), language="de")

    # print("Generating trigrams...")
    # process_dir(output_dir, trigram_dir)

    # print("Preprocessing complete")

    # print("Computing language profiles...")
    # generate_trigram_vectors(trigram_dir)
    # compute_language_vectors(trigram_dir)

    test_text = "My name is Tigran. I have been born and raised in Armenia"
    detected_language, similarity = detect_language(test_text)
    
    if detected_language:
        print(f"Detected Language: {detected_language} (Similarity: {similarity:.4f})")
    else:
        print("Language detection failed.")

if __name__ == '__main__':
    main()