import requests as req
from json import loads, dumps

filename = "22_16331.xls"
URL = "http://127.0.0.1"
PORT = "8001"


r = req.get(f"{URL}:{PORT}/memes/file/{filename}")
print(r.content)
contents = loads(r.text)
link = contents["link"]

r = req.get(f"{URL}:{PORT}/{link}")
print(r.status_code)
if r.status_code == 200:
    with open(filename, "wb") as f:
        f.write(r.content)