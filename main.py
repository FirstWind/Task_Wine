from http.server import HTTPServer, SimpleHTTPRequestHandler
import sys
from datetime import date
import pandas

from jinja2 import Environment, FileSystemLoader, select_autoescape

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')

excel_data_df = pandas.read_excel(
    'wine3.xlsx', sheet_name='Лист1',
    na_values=['N/A', 'NA'], keep_default_na=False
)
category_wine = "Категория"
list_wines = excel_data_df.to_dict(orient='records')
key_dict = sorted(set(excel_data_df[category_wine].tolist()))

new_wine = {}
for key in key_dict:
    list_category = []
    for key_list in list_wines:
        if key == key_list[category_wine]:
            list_category.append(key_list)
    new_wine[key] = list_category

age = date.today().year - 1920

if age % 10 == 1 and age != 11 and age % 100 != 11:
    age = f"{age} год"
elif 1 < age % 10 <= 4 and age != 12 and age != 13 and age != 14:
    age = f"{age} года"
else:
    age = f"{age} лет"

rendered_page = template.render(wines=new_wine, age=age)
with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

HandlerClass = SimpleHTTPRequestHandler
ServerClass = HTTPServer
Protocol = "HTTP/1.0"

if sys.argv[1:]:
    port = int(sys.argv[1])
else:
    port = 8000
server_address = ('127.0.0.1', port)

HandlerClass.protocol_version = Protocol
httpd = ServerClass(server_address, HandlerClass)

sa = httpd.socket.getsockname()
print("Serving HTTP on", sa[0], "port", sa[1], "...")
httpd.serve_forever()