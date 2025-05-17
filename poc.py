# Custom markdown parser: Extending markdown to cover CSS styling to implement a markdown parser
# Markdown syntax
# Bold: *, Italic: _, Heading: #, ##, ..., Link: ^, Ordered List: <, Unordered List: >, Images: ~, Escaped Char: \, Custom Formatting: |css_property value.

# Input file
from supabase import client, create_client
from config import secret, url
import re

# Global var
supabase_url = url
supabase_secret = secret

# Regex patterns
REGEX_PATTERN = [
# Bold
(r'\*(.+?)\*', 'bold')
# Italic
# Heading
# Link
# List
# Images
# Escaped Char
# Custom Formatting
]


def retrieve_file(file_name, bucket):
  supabase = create_client(supabase_url, supabase_secret)
  try:
    file_bytes = supabase.storage.from_(bucket).download(f'{file_name}.txt').decode("utf-8")
    print("Successfully retrieved file.")
    return file_bytes
  except Exception as e:
    print(f"Error: {e}")
    return 0

# in line formatting for bold, italic etc. so that i can append the entire line to paragraph to preserve hierarchy easier 
def inline_formatter(match, line, token_type):
    match_result = match
    text_value = match_result.groups()[0]
    if token_type == 'bold':
      line = line.replace(f"*{text_value}*", f"<strong>{text_value}</strong>")
    return line

# Splitting into words
def broad_parser(file_bytes):
  lines = file_bytes.splitlines()
  tokens = []
  # AST looks like [{token_type = '', value = ''}]
  current_paragraph = []
  for line in lines:
    line_data = line.strip()
    for pattern, token_type in REGEX_PATTERN:
      if token_type in ('header', 'custom_format'):
        match = re.match(pattern, line_data)
      else:
        match = re.search(pattern, line_data)

      if match: 
        line_data = inline_formatter(match, line_data, token_type)
      else:
        continue
      
    print(line_data)
    current_paragraph.append(line_data)

    if current_paragraph: 
        sentence = current_paragraph
        tokens.append({
        "type" : 'paragraph',
        "value" : sentence,
        })
        current_paragraph = []
  print("Data parsed and AST created.")
  print("AST: ", tokens)
  #checking for each line


file_name = "mybook"
bucket = "txt2epub"
file_data = retrieve_file(file_name, bucket)
if file_data:
  ast = broad_parser(file_data)
  print(ast)
