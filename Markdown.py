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
    bias = 0.5
    style = 1
    stroke_color = 'black'
    stroke_width = 1

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
Dear Ashley:
Merry Christmas.
Love,
Jonathan
"""

write_handwriting_from_markdown(markdown_content, 'Ashleytextbody.svg')
