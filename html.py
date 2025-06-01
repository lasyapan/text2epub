
def html_generation(ast):
    return ''.join(render(node) for node in ast)

def children_generation(children):
    return ''.join(render(child) for child in children)

def render(node):
    type = node.get('type')
    if type == 'header':
        return header_html(node)
    elif type == 'paragraph':
        return paragraph_html(node)
    elif type == 'image':
        return image_html(node)
    elif type == 'link':
        return link_html(node)
    elif type == 'unordered_list':
        return ul_html(node)
    elif type == 'bold':
        return bold_html(node)
    elif type == 'italic':
        return italic_html(node)
    else:
        return unknown_html(node)
    
def unknown_html(node):
    return ''

def header_html(node):
    level = node.get('level')
    value = node.get('value')
    return f'<h{level}> {value} </h{level}>'

def paragraph_html(node):
    children = node.get('children', [])
    children_content = children_generation(children)
    if children and all(child.get('type') == 'unordered_list' for child in children):
        return f'<ul> {children_content} </ul>'
    return f'<p> {children_content} </p>'

def link_html(node):
    link = node.get('link')
    text = node.get('text')
    return f'<a href="{link}"> {text} </a>'

def image_html(node):
    url = node.get('url')
    alt = node.get('alt')
    return f'<img src="{url}" alt="{alt}">'

def italic_html(node):
    value = node.get('value')
    return f'<i> {value} </i>'

def bold_html(node):
    value = node.get('value')
    return f'<b> {value} </b>'

def ul_html(node):
    value = node.get('value')
    return f'<li> {value} </li>'
