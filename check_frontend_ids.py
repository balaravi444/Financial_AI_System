import re
from pathlib import Path

root = Path('static')
html = root / 'index.html'
js = root / 'app.js'

html_text = html.read_text(encoding='utf-8')
js_text = js.read_text(encoding='utf-8')

ids_html = set(re.findall(r'id="([^"]+)"', html_text))
ids_js = set(re.findall(r'getElementById\(["\']([^"\']+)["\']\)', js_text))
ids_js |= set(re.findall(r'querySelector\(["\']#([^"\']+)["\']\)', js_text))

missing_in_html = sorted(i for i in ids_js if i not in ids_html)
unused_html = sorted(i for i in ids_html if i not in ids_js)

routes = sorted(set(re.findall(r'fetch\(["\'](/[^"\']*)["\']', js_text)))

print('HTML IDs:', len(ids_html))
print('JS IDs:', len(ids_js))
print('Missing in HTML:', missing_in_html)
print('Unused HTML IDs count:', len(unused_html))
print('Unused HTML IDs sample:', unused_html[:50])
print('Routes in JS:', routes)
