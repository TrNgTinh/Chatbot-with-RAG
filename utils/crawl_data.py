import argparse
import requests
from bs4 import BeautifulSoup
import os

def convert_to_markdown(tag):
    """
    Convert HTML tags to Markdown format.
    Args:
        tag (bs4.Tag): BeautifulSoup Tag representing an HTML element.
    Returns:
        str: Markdown-formatted
    """
    # Check if the tag is an 'h2' with class 'chakra-heading'
    if tag.name == 'h2' and 'chakra-heading' in tag.get('class', []):
        return f"\n# {tag.get_text(strip=True)}\n"
    elif tag.name == 'i' and 'chakra-heading' in tag.get('class', []):
        return f"\n## {tag.get_text(strip=True)}\n"
    elif tag.name == 'p' and 'chakra-text' in tag.get('class', []):
        return f"{tag.get_text(strip=True)}\n"
    elif tag.name == 'li':
        return f"\n- {tag.get_text(strip=True)}\n"
    elif tag.name == 'ul' and 'css-i1js5q' in tag.get('class', []):
        return '\n'.join([f"- {li.get_text(strip=True)}" for li in tag.find_all('li')])
    else:
        # Return an empty string for unsupported tags
        return ''

if __name__ == "__main__":
    # Use argparse to parse command line arguments
    parser = argparse.ArgumentParser(description="Convert HTML to Markdown")
    parser.add_argument("url", help="URL of the website", default="https://www.presight.io/privacy-policy.html", nargs='?')
    parser.add_argument("output_file", help="Name of the output Markdown file", default="output.md", nargs='?')
    args = parser.parse_args()

    # Get HTML content from the website
    response = requests.get(args.url)
    html = response.text

    # Use BeautifulSoup to extract text from HTML
    soup = BeautifulSoup(html, "html.parser")
    # Check and create the "data" directory if it doesn't exist
    if not os.path.exists("data"):
        os.makedirs("data")
    
    # Concatenate the results
    markdown_output = ''.join([convert_to_markdown(tag) for tag in soup.find_all(['div', 'h2', 'p', 'ul','i','li']) if convert_to_markdown(tag)])

    # Save the Markdown content to a file in the "data" directory
    output_path = os.path.join("data", args.output_file)
    with open(output_path, "w", encoding="utf-8") as file:
        file.write(markdown_output)

    print(f"Markdown content has been saved to '{output_path}'")

#Usage
#python utils/crawl_data.py https://www.presight.io/privacy-policy.html data/output.md
