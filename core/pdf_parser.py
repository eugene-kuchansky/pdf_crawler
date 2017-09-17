from pdfminer.pdfparser import PDFParser, PDFSyntaxError
from pdfminer.pdfpage import PDFPage


def pdf_parse(fp):
    links = []
    try:
        for page in PDFPage.get_pages(fp):
            for annot in page.annots:
                link = annot.resolve()
                if link['A']['URI'].lower().startswith('http'):
                    links.append(link['A']['URI'])
    except PDFSyntaxError:
        return None
    
    return links
