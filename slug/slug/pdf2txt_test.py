from pdfminer.pdfinterp import PDFResourceManager, process_pdf
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from io import StringIO
from io import open
import os

def read_pdf(pdfFile):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)

    process_pdf(rsrcmgr, device, pdfFile)
    device.close()

    content = retstr.getvalue()
    retstr.close()
    return content


if __name__ == '__main__':
    current_dir = os.path.dirname(__file__)
    patent_dir = os.path.join(current_dir, "patent")
    pdf=os.path.join(patent_dir,"AT285813B.pdf")
    print(pdf)
    content = read_pdf(open(pdf, 'rb'))
    with open("AT285813B.txt","a",encoding="utf8") as ff:
        ff.write(content)
