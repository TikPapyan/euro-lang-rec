from bs4 import BeautifulSoup
import os

input = 'europarl/txt'
output = 'de_xml_txt'

def de_xml_file(file_path, output_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
    except UnicodeDecodeError:
        with open(file_path, 'r', encoding='latin-1') as file:
            content = file.read()
    
    soup = BeautifulSoup(content, "html.parser")
    text = soup.get_text()
    
    with open(output_path, 'w', encoding='utf-8') as output_file:
        output_file.write(text)

def de_xml_directory(directory_path, output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.txt'):
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(root, directory_path)
                output_subdir = os.path.join(output_directory, relative_path)
                
                if not os.path.exists(output_subdir):
                    os.makedirs(output_subdir)
                
                output_file_path = os.path.join(output_subdir, file)
                de_xml_file(file_path, output_file_path)

de_xml_directory(input, output)