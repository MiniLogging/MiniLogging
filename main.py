import re
import jsbeautifier
from requests import session
requests = session()

mainsite = requests.get('https://miniblox.io').text

def use_regex(input_text):
    pattern = re.compile(r'/[^"]*\.js', re.IGNORECASE)
    return pattern.search(input_text).group()

for line in mainsite.split('\n'):
    if '"/assets/' in line and '.js' in line:
        js_name = use_regex(line.strip())
        link = f'https://miniblox.io{js_name}'

js_code_raw = requests.get(link)
changed_day = js_code_raw.headers['last-modified']
js_code = js_code_raw.text

# imma save github some work and not deal with formatting if not needed
try:
    with open('gamecode/index.js','r', encoding="utf-8") as f:
        old_js_code = f.read()
        if js_code == old_js_code: exit()
except FileNotFoundError:
    pass


with open('gamecode/index.js','w', encoding="utf-8") as f:
    f.write(js_code)

with open('gamecode/index formatted.js','w', encoding="utf-8") as f:
    formatted_code = jsbeautifier.beautify(js_code)
    f.write(formatted_code)

with open('temp_commit.txt','w') as f:
    data = f'{changed_day} {js_name}'
    print(data)
    f.write(data)
