import requests
import json

if __name__ == '__main__':
    headers = {'Host': 'worldwide.espacenet.com',
               'Connection': 'keep-alive',
               'Accept': 'application/json,application/i18n+xml',
               'X-EPO-PQL-Profile': 'cpci',
               'EPO-Trace-Id': '95jq2r-w6prc0-AAA-000001',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
               'Content-Type': 'application/json;charset=UTF-8',
               'Origin': 'https://worldwide.espacenet.com',
               'Sec-Fetch-Site': 'same-origin',
               'Sec-Fetch-Mode': 'cors',
               'Sec-Fetch-Dest': 'empty',
               'Referer': 'https://worldwide.espacenet.com/patent/search?q=A61K38%2F00',
               'Accept-Encoding': 'gzip, deflate, br',
               'Accept-Language': 'zh-CN,zh;q=0.9'
               }

    base_url = "https://worldwide.espacenet.com/3.2/rest-services/search?lang=en%2Cde%2Cfr&q=A61K38%2F00&qlang=cql&p_s=espacenet&p_q=A61K38%2F00"

data = {"query": {"fields": ["publications.ti_*", "publications.abs_*", "publications.pn_docdb", "publications.in",
                             "publications.in_country", "publications.pa", "publications.pa_country", "publications.pd",
                             "publications.pr_docdb", "publications.app_fdate.untouched", "publications.ipc",
                             "publications.ipc_ic", "publications.ipc_icci", "publications.ipc_iccn",
                             "publications.ipc_icai", "publications.ipc_ican", "publications.ci_cpci",
                             "publications.ca_cpci", "publications.cl_cpci",
                             "biblio:pa;pa_orig;pa_unstd;in;in_orig;in_unstd;pa_country;in_country;pd;pn;allKindCodes;",
                             "oprid_full.untouched", "opubd_full.untouched"], "from": 0, "size": 20, },
        "filters": {"publications.patent": [{"value": ["true"]}]}, "widgets": {}}

# print(json.loads(data))
proxy = {"https": "http://127.0.0.1:8888", "http": "http://127.0.0.1:8888"}
#

response = requests.post(url=base_url, data=json.dumps(data), headers=headers, verify=False, proxies=proxy)
#print(len(response.json()["hits"]))
response_json=response.json()
doc_num=len(response_json["hits"])
for i in range(doc_num):
    print(response_json["hits"][i]["familyNumber"])
    print(response_json["hits"][i]["hits"][0]["fields"]["publications.pn_docdb"][0])

#print(response.status_code)
