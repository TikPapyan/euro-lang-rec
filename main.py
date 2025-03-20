from preprocess import de_xml_dir, process_dir
from hdc import generate_trigram_vectors, compute_language_vectors, detect_language

input_dir = 'txt'
output_dir = 'de_xml_txt'
trigram_dir = 'trigrams'

def main():
    # print("De-XMLing files...")
    # de_xml_dir(input_dir, output_dir)

    # print("Generating trigrams...")
    # process_dir(output_dir, trigram_dir)

    # print("Preprocessing complete")

    # print("Computing language profiles...")
    # generate_trigram_vectors(trigram_dir)
    # compute_language_vectors(trigram_dir)

    test_text = "Bonjour, comment allez-vous aujourd'hui ?"
    detected_language, similarity = detect_language(test_text)
    
    if detected_language:
        print(f"Detected Language: {detected_language} (Similarity: {similarity:.4f})")
    else:
        print("Language detection failed.")

if __name__ == '__main__':
    main()