# Simple tool that replaces all single braces with double braces in an HTML file
# Use when embedding HTML in a Python string
import argparse
import os

def replace_curly_braces(html_file):
    with open(html_file, 'r') as f:
        html_data = f.read()

    html_data = html_data.replace('{', '{{').replace('}', '}}')

    new_filename = f'{os.path.splitext(html_file)[0]}_doublebraces.html'

    with open(new_filename, 'w') as f:
        f.write(html_data)

    print(f'Curly braces replaced with double curly braces in {html_file}, and saved to {new_filename}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Replace curly braces with double curly braces in an HTML file')
    parser.add_argument('html_file', type=str, help='Path to HTML file')
    args = parser.parse_args()

    replace_curly_braces(args.html_file)
