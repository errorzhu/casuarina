import requests
import json
import os

current_dir = os.path.dirname(__file__)


class PatentMenuGetter():
    def __init__(self):
        self.base_url = "https://worldwide.espacenet.com/3.2/rest-services/search?lang=en%2Cde%2Cfr&q=A61K38%2F00&qlang=cql&p_s=espacenet&p_q=A61K38%2F00"
        self.headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
            'Content-Type': 'application/json',
            #'EPO-Trace-Id': 's347yb-89q317-AAA-000000',
            'X-EPO-PQL-Profile': 'cpci',
            'Origin': 'https://worldwide.espacenet.com',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty'

            }

    def request(self, param, data):
        session = requests.session()
        url = self.base_url
        session.head("https://worldwide.espacenet.com/patent/?EPOTraceID=igd8d7-u7u4s5&event=onSearchSubmit_adv-off&lgCC=en_EP&listView=text-only")
        response = session.post(url, headers=self.headers, data=json.dumps(data), verify=False)
        print(response.text)


if __name__ == '__main__':
    with open(os.path.join(current_dir, "tests", "resources", "menu_get_parameter.json"), 'r', encoding="utf8") as f:
        request_parameter = "".join(f.readlines())
        parameter = json.loads(request_parameter)
    getter = PatentMenuGetter()
    getter.request("A61K38%2F00", parameter)
