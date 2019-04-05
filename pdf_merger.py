from PyPDF2 import PdfFileMerger
from os import listdir
from os.path import isfile, join


def main():
    # get list of all pdf files
    pdfs = [join('pdfs', f) for f in listdir('pdfs') if isfile(join('pdfs', f))]
    # print(pdfs)

    merger = PdfFileMerger()
    
    for pdf in pdfs:
        merger.append(pdf)
    
    merger.write('all_sheets.pdf')


if __name__ == '__main__':
    main()
