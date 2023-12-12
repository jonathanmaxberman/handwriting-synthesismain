from flask import Flask, request, render_template, url_for
import markdown
from bs4 import BeautifulSoup
from demo import Hand  # Make sure this import works based on your project structure

app = Flask(__name__)

def markdown_to_text(md_content):
    """Convert Markdown content to plain text."""
    html = markdown.markdown(md_content)
    soup = BeautifulSoup(html, features="html.parser")
    return soup.get_text("\n", strip=True)

def write_handwriting_from_markdown(md_content, filename, biases, styles):
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
        stroke_widths=stroke_widths
    )


@app.route('/', methods=['GET', 'POST'])
def index():
    image_file = None
    if request.method == 'POST':
        md_content = request.form['md_text']
        biases = [float(request.form.get('bias', 0.75))]
        styles = [int(request.form.get('style', 9))]

        # Repeat the bias and style for each line
        lines = md_content.split('\n')
        biases *= len(lines)
        styles *= len(lines)

        output_file = 'static/handwriting_output.svg'
        write_handwriting_from_markdown(md_content, output_file, biases, styles)
        image_file = url_for('static', filename='handwriting_output.svg')

    return render_template('index.html', image_file=image_file)


if __name__ == '__main__':
    app.run(debug=True)
