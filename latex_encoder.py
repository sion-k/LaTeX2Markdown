from latex2svg import latex2svg
import base64
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import io

plt.rcParams.update({
    "text.usetex": True,
    "font.family": "Helvetica"
})


def encode(latex: str):
    """
    Encodes a LaTeX into svg
    Encodes a svg into base64.
    """
    svg = latex_to_svg(latex)
    return svg2base64(svg)


def color_white(svg: str):
    # Parse the SVG string
    root = ET.fromstring(svg)

    # Find all path elements and change their fill color
    path_elements = root.findall(".//{http://www.w3.org/2000/svg}path")
    for path_element in path_elements:
        path_element.set("fill", "white")

    # Return the modified SVG as a string
    modified_svg = ET.tostring(root, encoding="unicode")
    return modified_svg


def svg2base64(svg_code: str):
    svg_bytes = svg_code.encode('utf-8')
    base64_encoded = base64.b64encode(svg_bytes)
    base64_string = base64_encoded.decode('utf-8')

    return base64_string


def latex_to_svg(latex_code, font_size=12):
    # Calculate height and width based on font size
    height = font_size / 72  # Convert font size from points to inches
    # Assume average character width of font_size/2
    width = len(latex_code) * (font_size / 2) / 72

    fig, ax = plt.subplots(figsize=(width, height))
    ax.text(0.5, 0.5, f'${latex_code}$', fontsize=font_size,
            ha='center', va='center', transform=ax.transAxes, color='white')

    # Remove margins and borders
    ax.margins(0)
    ax.set_axis_off()

    # Save the plot as SVG
    svg_buffer = io.BytesIO()
    plt.savefig(svg_buffer, format='svg', transparent=True,
                bbox_inches='tight', pad_inches=0)
    plt.close(fig)

    # Retrieve the SVG code
    svg_code = svg_buffer.getvalue().decode()

    return svg_code


# Example usage
# latex_equation = r'\frac{{d}}{{dx}}(x^2) = 2x'
# svg_equation = latex_to_svg(latex_equation)
# print(svg_equation)
