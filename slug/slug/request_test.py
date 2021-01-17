import requests

if __name__ == '__main__':
    # data={"query":{"fields":["publications.ti_*","publications.abs_*","publications.pn_docdb","publications.in","publications.in_country","publications.pa","publications.pa_country","publications.pd","publications.pr_docdb","publications.app_fdate.untouched","publications.ipc","publications.ipc_ic","publications.ipc_icci","publications.ipc_iccn","publications.ipc_icai","publications.ipc_ican","publications.ci_cpci","publications.ca_cpci","publications.cl_cpci","biblio:pa;pa_orig;pa_unstd;in;in_orig;in_unstd;pa_country;in_country;pd;pn;allKindCodes;","oprid_full.untouched","opubd_full.untouched"],"from":0,"size":20,"highlighting":[{"field":"publications.ti_en","fragment_words_number":20,"number_of_fragments":3,"hits_only":True},{"field":"publications.abs_en","fragment_words_number":20,"number_of_fragments":3,"hits_only":True},{"field":"publications.ti_de","fragment_words_number":20,"number_of_fragments":3,"hits_only":True},{"field":"publications.abs_de","fragment_words_number":20,"number_of_fragments":3,"hits_only":True},{"field":"publications.ti_fr","fragment_words_number":20,"number_of_fragments":3,"hits_only":True},{"field":"publications.abs_fr","fragment_words_number":20,"number_of_fragments":3,"hits_only":True},{"field":"publications.pn","fragment_words_number":20,"number_of_fragments":3,"hits_only":True},{"field":"publications.pn_docdb","fragment_words_number":20,"number_of_fragments":3,"hits_only":True},{"field":"publications.pa","fragment_words_number":20,"number_of_fragments":3,"hits_only":True}]},"filters":{"publications.patent":[{"value":["true"]}]},"widgets":{}}
    # session = requests.session()
    # session.get("https://worldwide.espacenet.com/patent/search?q=A61K38%2F00")
    # session.head("https://worldwide.espacenet.com/patent/?EPOTraceID=42nto7-3geaht&event=ApplicationStartup&lgCC=en_EP&pathname=%2Fpatent%2Fsearch&search=%3Fq%3DA61K38%252F00&called_by=NA")
    # response = session.post("https://worldwide.espacenet.com/3.2/rest-services/search?lang=en%2Cde%2Cfr&q=A61K38%2F00&qlang=cql&p_s=espacenet&p_q=A61K38%2F00",data=data)

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
        'Referer': 'https://worldwide.espacenet.com/patent/search/family/026602061/publication/EP1329508A1?q=EP1329508A1',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }

    # proxy = {"https": "http://127.0.0.1:8888","http": "http://127.0.0.1:8888"}
    # proxies = proxy

    response = requests.get(
        'https://worldwide.espacenet.com/3.2/rest-services/images/documents/EP/1329508/A1/formats/pdf/pages/?EPO-Trace-Id=tp34mw-9nuttg-XXX-000009',
        verify=False, headers=headers
    )
    with open("test2.pdf", 'wb') as ff:
        ff.write(response.content)
