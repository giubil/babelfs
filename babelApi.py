import requests
import re

class BabelApi:
    def __init__(self):
        self.url = "http://libraryofbabel.info/"

    def search(self, data_block):
        payload = {"btnSubmit": "Search",
                   "method": "x",
                   "find": data_block}
        r = requests.post(self.url + "search.cgi", data=payload)
        matches = re.findall('postform\(.*\)', r.text)
        elem = matches[0]
        elem = elem.split("postform(")[1].split(')')[0].split(',')
        data = {"hex": elem[0][1:-1],
                "wall": int(elem[1][1:-1]),
                "shelf": int(elem[2][1:-1]),
                "volume": int(elem[3][1:-1]),
                "page": int(elem[4][1:-1]),
                "len": len(data_block)}
        return data

    def lookup(self, data_struct):
        r = requests.post(self.url + "book.cgi", data=data_struct)
        return r.text.split('<PRE id = "textblock">')[1].split('</PRE>')[0].replace('\n', '')[:data_struct["len"]]