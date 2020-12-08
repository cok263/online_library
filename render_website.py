import os
import json
import math
from jinja2 import Environment, FileSystemLoader, select_autoescape
from http.server import HTTPServer, SimpleHTTPRequestHandler
from livereload import Server
from more_itertools import chunked


BOOKS_ON_PAGE_COUNT = 10
COLUMN_BOOKS_COUNT = 2


def on_reload():
    os.makedirs('pages', exist_ok=True)

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html'])
    )

    template = env.get_template('template.html')
    with open('download/books.json', 'r') as lib_file:
        books_json = lib_file.read()
    books = json.loads(books_json)
    for num_page, books_page in enumerate(list(chunked(books, BOOKS_ON_PAGE_COUNT)), 1):
        rendered_page = template.render(
            books=list(chunked(books_page, COLUMN_BOOKS_COUNT)),
            pages_count=math.ceil(len(books) / BOOKS_ON_PAGE_COUNT),
            current_page=num_page,
        )
        with open(
            f'pages/index{num_page}.html', 'w', encoding="utf8"
        ) as file:
            file.write(rendered_page)
        print('template reloaded')


def main():
    on_reload()

    server = Server()
    server.watch('template.html', on_reload)
    server.serve(root='.')


if __name__ == '__main__':
    main()
