import requests
from os import getcwd, path
from io import BytesIO

if path.exists("../Kawi") and 0:
    url = "https://raw.githubusercontent.com/lenaEla/LenapyShopMsg/main/shopMsg.py"
    directory = getcwd()
    filename = directory + '\shopMsg.py'
    print(filename)
    r = requests.get(url)

    f = open(filename,'wb')
    write_byte = BytesIO(r.content)
    f.write(write_byte.getbuffer())
    f.close()