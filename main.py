from storagefunc import initialise_gcp, upload_file, retrieve_file
from poc import broad_parser
from html import html_generation

client, bucket = initialise_gcp()
print('Initialised')

file_name = 'mybook.txt'
if file_name:
    try:
        file_data = retrieve_file(file_name, bucket)
        text_content = file_data.decode("utf-8")
        ast = broad_parser(text_content)
        html = html_generation(ast)
        print(html)
    except Exception as e:
        print(e)

