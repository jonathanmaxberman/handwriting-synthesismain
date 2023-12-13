from flask import Flask, request, render_template, url_for
import markdown
from bs4 import BeautifulSoup
from demo import Hand  # Make sure this import works based on your project structure
import re
import xml.etree.ElementTree as ET
import time

app = Flask(__name__)

def remove_initial_m0(svg_path):
    # Load the SVG file
    tree = ET.parse(svg_path)
    root = tree.getroot()

    # Namespace for SVG
    ns = {'svg': 'http://www.w3.org/2000/svg'}

    # Regex to match 'M0,0' or variations
    m0_pattern = re.compile(r'^\s*M\s*0\s*,?\s*0\s+')

    # Iterate through all 'path' elements
    for path in root.findall('.//svg:path', ns):
        d = path.get('d')
        # Remove the initial 'M0,0' if present
        new_d = m0_pattern.sub('', d)
        path.set('d', new_d)

    # Save the modified SVG
    tree.write(svg_path)


def markdown_to_text(md_content):
    """Convert Markdown content to plain text."""
    html = markdown.markdown(md_content)
    soup = BeautifulSoup(html, features="html.parser")
    return soup.get_text("\n", strip=True)


def write_handwriting_from_markdown(md_content, filename, biases, styles, left_justify):
    """Generate handwriting from Markdown content."""
    text = markdown_to_text(md_content)
    lines = text.split('\n')

    # Ensure biases and styles lists are the same length as lines
    # If not, repeat or truncate the biases and styles to match the number of lines
    biases = (biases * len(lines))[:len(lines)]
    styles = (styles * len(lines))[:len(lines)]

    stroke_colors = ['black' for _ in lines]  # Fixed color as black
    stroke_widths = [1 for _ in lines]        # Fixed width as 1

    hand = Hand()
    hand.write(
        filename=filename,
        lines=lines,
        biases=biases,
        styles=styles,
        stroke_colors=stroke_colors,
        stroke_widths=stroke_widths,
        left_justify=left_justify
    )
    #remove_initial_m0(filename)

@app.route('/', methods=['GET', 'POST'])
def index():
    image_file = None
    if request.method == 'POST':
        md_content = request.form['md_text']
        left_justify = 'left_justify' in request.form
        biases = [float(request.form.get('bias', 0.75))]
        styles = [int(request.form.get('style', 22))]

        # Repeat the bias and style for each line
        lines = md_content.split('\n')
        biases *= len(lines)
        styles *= len(lines)

        output_file = 'static/handwriting_output.svg'
        write_handwriting_from_markdown(md_content, output_file, biases, styles, left_justify)

        timestamp = int(time.time())
        image_file = url_for('static', filename='handwriting_output.svg') + f'?v={timestamp}'

    return render_template('index.html', image_file=image_file)


if __name__ == '__main__':
    app.run(debug=True)
