import requests
import string
from multiprocessing import Process, Pool

headers = {
    'Host': 'worldwide.espacenet.com',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'Referer': 'https://worldwide.espacenet.com/patent/search/family/026602061/publication/WO9815179A1?q=WO9815179A1',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}

base_url = "https://worldwide.espacenet.com/3.2/rest-services/images/documents/{0}/{1}/{2}/formats/pdf/pages/?EPO-Trace-Id=tp34mw-9nuttg-XXX-000009"


def parse_patent_number(patent_number):
    f1 = patent_number[:2]
    if patent_number[-1] in string.digits:
        f2 = patent_number[2:-2]
        f3 = patent_number[-2:]
    else:
        f2 = patent_number[2:-1]
        f3 = patent_number[-1]
    return (f1, f2, f3)


def download_one_patent(patent_number):
    number = parse_patent_number(patent_number)
    url = base_url.format(number[0], number[1], number[2])
    print(url)
    response = requests.get(
        url,
        verify=False, headers=headers
    )
    with open(patent_number + ".pdf", 'wb') as ff:
        ff.write(response.content)
    print(patent_number + "  download success ")


def download(menu_file):
    with open(menu_file, "r", encoding="utf8") as ff:
        line = ff.readline()
        while line:
            download_one_patent(line.strip())
            line = ff.readline()
            index = index + 1


def write2sub_patent_menu(menu_file, content):
    with open(menu_file, "a", encoding="utf8") as ff:
        ff.write(content)
        ff.write("\n")


def split_menu_file(menu_file, num):
    with open(menu_file, "r", encoding="utf8") as ff:
        line = ff.readline()
        index = 0
        while line:
            write2sub_patent_menu(menu_file + "_" + str(index % num), line.strip())
            line = ff.readline()
            index = index + 1
        ff.close()


if __name__ == '__main__':
    patent_menu_file = "patent_menu"
    process_number = 4
    split_menu_file(patent_menu_file, process_number)
    p = Pool(process_number)
    for i in range(process_number):
        menu_file = patent_menu_file + "_" + str(i)
        p.apply(download, args=(menu_file,))
