import os
import glob

# Specify the directory containing the text files
directory = 'data/civic/extracted_data'

# Create a list to store the content of each file
merged_content = []

# Use glob to find all text files in the directory
text_files = glob.glob(os.path.join(directory, '*.txt'))

# Loop through each text file and read its content
for file_path in text_files:
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        merged_content.append(content)

# Join all contents into a single string with newline separation
merged_content = '\n'.join(merged_content)

# Specify the output file path
output_file = 'data/civic/merge_of_extracted_data/merged_output.txt'

# Write the merged content to the output file
with open(output_file, 'w', encoding='utf-8') as file:
    file.write(merged_content)

print(f'Merged {len(text_files)} files into {output_file}')
