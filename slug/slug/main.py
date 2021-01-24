import json
import requests
from urllib.parse import unquote, quote
import datetime, time

base_url = "https://worldwide.espacenet.com/3.2/rest-services/search?lang=en%2Cde%2Cfr&q={0}&qlang=cql&p_s=espacenet&p_q={1}"
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
           'Referer': 'https://worldwide.espacenet.com/patent',
           'Accept-Encoding': 'gzip, deflate, br',
           'Accept-Language': 'zh-CN,zh;q=0.9'
           }

data = {"query": {"fields": ["publications.pn_docdb"], "from": 0, "size": 1000},
        "filters": {"publications.patent": [{"value": ["true"]}]}, "widgets": {}}


def format_base_url(ipc, start_date, end_date):
    template = 'cl = "{0}" AND pd within "{1},{2}"'
    variable = template.format(ipc, start_date, end_date)
    variable= quote(variable,safe='')
    url = base_url.format(variable, variable)
    return url


def write2file(file, content):
    with open(file, "a+", encoding="utf8") as ff:
        ff.write(content)
        ff.write("\n")


def get_all_patent_no_by_ipc(ipc):
    url = format_base_url(ipc)
    response = requests.post(url=url, data=json.dumps(data), headers=headers, verify=False)
    patent_num = int(response.json()["familiesNumber"])
    from_index = 0
    size = 1000
    file = "patent_menu"
    while (from_index + size < patent_num):
        data["query"]["from"] = 3000
        data["query"]["size"] = size
        print(data)
        response = requests.post(url=url, data=json.dumps(data), headers=headers, verify=False)
        response_json = response.json()
        doc_num = len(response_json["hits"])
        for i in range(doc_num):
            # print(response_json["hits"][i]["familyNumber"])
            write2file(file, response_json["hits"][i]["hits"][0]["fields"]["publications.pn_docdb"][0])
        from_index += size


if __name__ == '__main__':
    ipc = "A61K38/00"
    file = "patent_menu"
    size = 1000
    date_interval = []
    start_date = "2002-02-28"
    # end_date = "1975-12-31"
    date_interval.append(start_date)

    # date_interval.append(end_date)
    while (date_interval[-1] < datetime.datetime.today().strftime("%Y-%m-%d")):
        print(date_interval[-1])
        span = 15

        start_date = date_interval[-1]
        start_date_time = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        end_date = (start_date_time + datetime.timedelta(days=span)).strftime("%Y-%m-%d")
        # if(len(date_interval) ==1 ):
        #     end_date = "1973-01-01"
        url = format_base_url(ipc, start_date, end_date)
        #print(url)

        response = requests.post(url=url, data=json.dumps(data), headers=headers, verify=False)
        #print(response.text)
        response_json = response.json()
        #print(response_json)
        patent_num = int(response_json["familiesNumber"])
        if patent_num <= size:
            doc_num = len(response_json["hits"])
            for i in range(doc_num):
                # print(response_json["hits"][i]["familyNumber"])
                write2file(file, response_json["hits"][i]["hits"][0]["fields"]["publications.pn_docdb"][0])
            date_interval.append(end_date)
        else:
            while (patent_num > size):
                end_date = (start_date_time + datetime.timedelta(days=span)).strftime("%Y-%m-%d")
                url = format_base_url(ipc, start_date, end_date)
                response = requests.post(url=url, data=json.dumps(data), headers=headers, verify=False)
                patent_num = int(response.json()["familiesNumber"])
                span = int(span / 2)
            url = format_base_url(ipc, start_date, end_date)
            response = requests.post(url=url, data=json.dumps(data), headers=headers, verify=False)
            response_json = response.json()
            patent_num = int(response_json["familiesNumber"])
            doc_num = len(response_json["hits"])
            for i in range(doc_num):
                # print(response_json["hits"][i]["familyNumber"])
                write2file(file, response_json["hits"][i]["hits"][0]["fields"]["publications.pn_docdb"][0])
            date_interval.append(end_date)
