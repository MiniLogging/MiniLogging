import re
import jsbeautifier
from requests import session
requests = session()

mainsite = requests.get('https://miniblox.io').text

def use_regex(input_text):
    pattern = re.compile(r"index-[A-Za-z0-9]+\.js", re.IGNORECASE)
    return pattern.search(input_text).group()

for line in mainsite.split('\n'):
    if '"/assets/index-' in line and '.js' in line:
        link = f'https://miniblox.io/assets/{use_regex(line.strip())}'

js_code_raw = requests.get(link)
changed_day = js_code_raw.headers['last-modified']
js_code = js_code_raw.text

with open('gamecode/index.js','w', encoding="utf-8") as f:
    f.write(js_code)

with open('gamecode/index formated.js','w', encoding="utf-8") as f:
    formatted_code = jsbeautifier.beautify(js_code)
    f.write(formatted_code)

with open('temp_commit.txt','w') as f:
    data = f'{link} {changed_day}'
    print(data)
    f.write(data)
