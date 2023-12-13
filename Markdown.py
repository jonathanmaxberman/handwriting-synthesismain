import markdown
from bs4 import BeautifulSoup
from demo import Hand


def markdown_to_text(md_content):
    """Convert Markdown content to plain text."""
    html = markdown.markdown(md_content)
    soup = BeautifulSoup(html, features="html.parser")
    return soup.get_text("\n", strip=True)


def write_handwriting_from_markdown(md_content, filename):
    """Generate handwriting from Markdown content."""
    text = markdown_to_text(md_content)
    lines = text.split('\n')

    # Static parameters for handwriting style
    bias = 0.95
    style = 32
    stroke_color = 'black'
    stroke_width = 2

    hand = Hand()
    hand.write(
        filename=filename,
        lines=lines,
        biases=[bias] * len(lines),
        styles=[style] * len(lines),
        stroke_colors=[stroke_color] * len(lines),
        stroke_widths=[stroke_width] * len(lines)
    )


# Example usage
markdown_content = """
Take a break 4mg
one tab   PR q4h
Disp 30 (thirty)

J Berman 12-13-23
"""

write_handwriting_from_markdown(markdown_content, 'script.svg')
