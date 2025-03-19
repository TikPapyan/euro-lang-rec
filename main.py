from preprocess import de_xml_dir, process_dir
from hdc import generate_trigram_vectors, compute_language_vectors

input_dir = 'europarl/txt'
output_dir = 'de_xml_txt'
trigram_dir = 'trigrams'

def main():
    # print("De-XMLing files...")
    # de_xml_dir(input_dir, output_dir)

    # print("Generating trigrams...")
    # process_dir(output_dir, trigram_dir)

    # print("Preprocessing complete!")

    print("Computing language profiles...")
    trigram_vectors = generate_trigram_vectors('trigrams')
    language_vectors = compute_language_vectors('trigrams')

if __name__ == '__main__':
    main()