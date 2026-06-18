import urllib.request

urls = [
    'http://127.0.0.1:8000/',
    'http://127.0.0.1:8000/health',
    'http://127.0.0.1:8000/static/index.html'
]

for url in urls:
    try:
        with urllib.request.urlopen(url, timeout=5) as r:
            print(url)
            print('STATUS', r.status)
            print('CONTENT-TYPE', r.getheader('Content-Type'))
            data = r.read(200)
            print('BODY', data.decode('utf-8', errors='replace'))
    except Exception as e:
        print(url, 'ERROR', type(e).__name__, e)
