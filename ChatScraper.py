"""from bs4 import BeautifulSoup
import os

# Define the folder path containing HTML files and the output text file
folder_path = '/Users/sm9276/PycharmProjects/PLEXOS-Help-Data/Html_Files'  # Replace with your folder path
file_path = 'extracted_data.txt'

# Function to extract content from a single HTML file
def extract_content_from_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extracting the header
    header = soup.find('h1').text.strip() if soup.find('h1') else 'No header found'

    # Extracting table data
    table_data = ''
    tables = soup.find_all('table')
    for table in tables:
        rows = table.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            if cols:
                # Use tabs to separate columns
                row_data = '\t'.join(col.text.strip() for col in cols)
                table_data += f"{row_data}\n"

    # Extracting paragraphs with clear separation
    paragraphs = soup.find_all('p')
    paragraph_data = '\n\n'.join(p.get_text(separator=' ', strip=True) for p in paragraphs)

    # Extracting lists with tabs for each item
    list_data = ''
    lists = soup.find_all('ul')
    for ul in lists:
        list_data += '\n'.join(f"\t- {li.get_text(separator=' ', strip=True)}" for li in ul.find_all('li')) + '\n'

    # Extracting additional headers (h2, h3, etc.)
    additional_headers = ''
    for tag in ['h2', 'h3', 'h4', 'h5', 'h6']:
        headers = soup.find_all(tag)
        if headers:
            additional_headers += f"\n{tag.upper()}s:\n"
            additional_headers += '\n'.join(header.get_text(strip=True) for header in headers) + '\n'

    # Formatting the extracted data
    content = f"Header: {header}\n\n"
    content += "Table Details:\n" + table_data + "\n"
    content += "Paragraphs:\n" + paragraph_data + "\n"
    content += "Lists:\n" + list_data + "\n"
    content += additional_headers

    return content

# Function to update the text file dynamically
def update_text_file(file_path, new_content):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            existing_content = file.read()

        # Add new content if not already present
        if new_content not in existing_content:
            with open(file_path, 'a') as file:
                file.write("\n--- New Page Data ---\n")
                file.write(new_content)
            print("Data has been appended to the file.")
        else:
            print("Content is already present in the file.")
    else:
        # Create the file and write the new content if it does not exist
        with open(file_path, 'w') as file:
            file.write(new_content)
        print("File created and data written.")

# Iterate through each HTML file in the specified folder
for filename in os.listdir(folder_path):
    if filename.endswith('.html'):
        file_path_html = os.path.join(folder_path, filename)

        # Read the HTML file
        with open(file_path_html, 'r', encoding='utf-8') as file:
            html_content = file.read()

        # Extract content from the HTML file
        page_content = extract_content_from_html(html_content)

        # Update the text file with the new content
        update_text_file(file_path, page_content)

print("All files have been processed.")

"""
from bs4 import BeautifulSoup
import os

# Define the folder paths for HTML files and output text files
input_folder_path = '/Users/sm9276/PycharmProjects/PLEXOS-Help-Data/Html_Files'  # Replace with your folder path
output_folder_path = '/Users/sm9276/PycharmProjects/PLEXOS-Help-Data/Extracted_Data'  # Replace with your desired output folder path

# Ensure the output folder exists
os.makedirs(output_folder_path, exist_ok=True)

# Function to extract content from a single HTML file
def extract_content_from_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extracting the header
    header = soup.find('h1').text.strip() if soup.find('h1') else 'No header found'

    # Extracting table data
    table_data = ''
    tables = soup.find_all('table')
    for table in tables:
        rows = table.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            if cols:
                # Use tabs to separate columns
                row_data = '\t'.join(col.text.strip() for col in cols)
                table_data += f"{row_data}\n"

    # Extracting paragraphs with clear separation
    paragraphs = soup.find_all('p')
    paragraph_data = '\n\n'.join(p.get_text(separator=' ', strip=True) for p in paragraphs)

    # Extracting lists with tabs for each item
    list_data = ''
    lists = soup.find_all('ul')
    for ul in lists:
        list_data += '\n'.join(f"\t- {li.get_text(separator=' ', strip=True)}" for li in ul.find_all('li')) + '\n'

    # Extracting additional headers (h2, h3, etc.)
    additional_headers = ''
    for tag in ['h2', 'h3', 'h4', 'h5', 'h6']:
        headers = soup.find_all(tag)
        if headers:
            additional_headers += f"\n{tag.upper()}s:\n"
            additional_headers += '\n'.join(header.get_text(strip=True) for header in headers) + '\n'

    # Formatting the extracted data
    content = f"Header: {header}\n\n"
    content += "Table Details:\n" + table_data + "\n"
    content += "Paragraphs:\n" + paragraph_data + "\n"
    content += "Lists:\n" + list_data + "\n"
    content += additional_headers

    return content

# Iterate through each HTML file in the specified folder
for filename in os.listdir(input_folder_path):
    if filename.endswith('.html'):
        file_path_html = os.path.join(input_folder_path, filename)

        # Read the HTML file
        with open(file_path_html, 'r', encoding='utf-8') as file:
            html_content = file.read()

        # Extract content from the HTML file
        page_content = extract_content_from_html(html_content)

        # Write the content to a new text file in the output folder
        output_file_path = os.path.join(output_folder_path, f"{os.path.splitext(filename)[0]}.txt")
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            output_file.write(page_content)

print("All files have been processed and saved.")
