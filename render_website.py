import json
from jinja2 import Environment, FileSystemLoader, select_autoescape
from http.server import HTTPServer, SimpleHTTPRequestHandler
from livereload import Server
from more_itertools import chunked


def on_reload():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html'])
    )

    template = env.get_template('template.html')
    with open('download/books.json', 'r') as lib_file:
        books_json = lib_file.read()
    books = json.loads(books_json)
    rendered_page = template.render(
        books=list(chunked(books, len(books // 2))),
    )
    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)
    print('template is reload')


on_reload()

server = Server()
server.watch('template.html', on_reload)
server.serve(root='.')
#server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
#server.serve_forever()