import bibtexparser
import re

# Paths to your files
bib_file_path = "./bib/references.bib"  # Update path to your .bib file
readme_file_path = "./README.md"

# Parse the .bib file
def parse_bib_file(bib_file):
    with open(bib_file, 'r') as bibtex_file:
        bib_database = bibtexparser.load(bibtex_file)
    return bib_database.entries

# Format the bibliography with numbering in markdown
def format_bibliography_with_numbers(bib_entries):
    numbered_bibliography = ""
    
    for i, entry in enumerate(bib_entries, start=1):
        # Format each entry depending on its type (article, book, etc.)
        if entry['ENTRYTYPE'] == 'article':
            numbered_bibliography += f"{i}. {entry.get('author', 'Unknown Author')}, \"{entry.get('title', 'No Title')}\", *{entry.get('journal', 'No Journal')}*, {entry.get('year', 'No Year')}, {entry.get('volume', '')}({entry.get('number', '')}), {entry.get('pages', '')}.\n\n"
        elif entry['ENTRYTYPE'] == 'book':
            numbered_bibliography += f"{i}. {entry.get('author', 'Unknown Author')}, *{entry.get('title', 'No Title')}*, {entry.get('publisher', 'No Publisher')}, {entry.get('year', 'No Year')}.\n\n"
        else:
            numbered_bibliography += f"{i}. {entry.get('author', 'Unknown Author')}, *{entry.get('title', 'No Title')}*, {entry.get('year', 'No Year')}.\n\n"
    
    return numbered_bibliography

# Update the bibliography section in README.md
def update_readme(readme_file, new_bibliography):
    with open(readme_file, 'r') as file:
        readme_content = file.read()
    
    # Find and replace the bibliography section
    updated_readme = re.sub(
        r'## Bibliography\n.*?(?=\n##|\Z)', 
        f"## Bibliography\n{new_bibliography}", 
        readme_content, 
        flags=re.DOTALL
    )
    
    with open(readme_file, 'w') as file:
        file.write(updated_readme)

# Parse and update
bib_entries = parse_bib_file(bib_file_path)
formatted_bibliography = format_bibliography_with_numbers(bib_entries)
update_readme(readme_file_path, formatted_bibliography)

print("README.md updated with the latest numbered bibliography.")