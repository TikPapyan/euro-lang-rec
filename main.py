from preprocess import de_xml_directory, process_directory

input_dir = 'europarl/txt'
output_dir = 'de_xml_txt'
trigram_dir = 'trigrams'

def main():
    # print("De-XMLing files...")
    # de_xml_directory(input_dir, output_dir)

    print("Generating trigrams...")
    process_directory(output_dir, trigram_dir)

    print("Preprocessing complete!")

if __name__ == '__main__':
    main()