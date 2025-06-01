# Custom markdown parser: Extending markdown to cover CSS styling to implement a markdown parser
# Markdown syntax
# Bold: *, Italic: _, Heading: #, ##, ..., Link: ^, Ordered List: <, Unordered List: >, Images: ~, Escaped Char: \, Custom Formatting: |css_property value.

# Input file
import re

# Regex patterns
REGEX_PATTERN = [
    # Bold
    (r'\*(.+?)\*', 'bold'),
    # Italic
    (r'_(.+?)_', 'italic'),
    # Unordered List
    (r'>\s(.+)', 'unordered_list'),
    # Header
    (r'^(#{1,6})\s(.+)', 'header'),
    #Link
    (r'\^(.+?) (.+?)\^', 'link'),
    #image
    (r'~(.+?)\s(.+?)~', 'image'),
    # custom formatting
    (r'\$(\w+)\s(.+)', 'custom_format') 
]


def inline_formatter(match, line, token_type):
    text_value = match.groups()[-1]
    if token_type == 'bold':
        line = line.replace(f"*{text_value}*", f"{text_value}")
    elif token_type == 'italic':
        line = line.replace(f"_{text_value}_", f"{text_value}")
    elif token_type == 'link':
        url, text_value = match.groups()
    return line

def broad_parser(file_bytes):
    try:
        lines = file_bytes.splitlines()
        print(lines)
        tokens = []
        current_paragraph = []

        for line in lines:
            if not line.strip():  # Empty line signals paragraph break
                if current_paragraph:
                    tokens.append({"type": "paragraph", "children": current_paragraph.copy()})
                    current_paragraph = []
                continue

            line_data = line.strip()
            print(line_data)
            children = []  # Stores inline formatting
            
            matched = False
            for pattern, token_type in REGEX_PATTERN:
                match = re.search(pattern, line_data)
                if match:
                    if token_type == 'header':
                        heading_level = len(match.groups())-1
                        text_value = match.groups()[1]
                        tokens.append({"type": "header", "level": heading_level, "value": text_value})
                    elif token_type == "image":
                        url, alt_text = match.groups()
                        children.append({"type": "image", "url": url, "alt": alt_text})
                    elif token_type == "css_style":
                        css_property, css_value = match.groups()
                        children.append({"type": "css_style", "property": css_property, "value": css_value})
                    elif token_type == 'link':
                        link, text = match.groups()
                        children.append({"type": "link", "link": link, "text": text})
                    elif token_type == 'unordered_list':
                        value = match.groups()
                        children.append({"type": "unordered_list", "value": value})
                    else:
                            text_value = match.groups()[-1]
                            line_data = inline_formatter(match, line_data, token_type)
                            children.append({"type": token_type, "value": line_data})
                    matched = True
            
            if not matched:
                children.append({"type": "text", "value": line_data})  # Store as plain text
            current_paragraph.extend(children)

        if current_paragraph:
                tokens.append({"type": "paragraph", "children": current_paragraph.copy()})

        print("Data parsed and AST created.")
        print("AST:", tokens)
        return tokens
    except Exception as e:
        raise(e)
