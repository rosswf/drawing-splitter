#!/usr/bin/env python3
"""A tool for splitting combined drawing PDF's into single files named
by drawing number.

USAGE
    python3 drawing_splitter.py dwg-number-element

    Where dwg-number-element is a part of the drawing number to be
    searched for.
"""
import re
import os
import sys
import warnings

import PyPDF2
import pdfplumber


def get_pdf_length(filename):
    """Return the number of pages of a PDF given it's file name."""
    with pdfplumber.open(filename) as pdf:
        num_of_pages = len(pdf.pages)
        return num_of_pages


def get_drawing_numbers(filename, num_of_pages, drawing_number_element):
    """Return a list of drawing numbers, read from each page of a PDF."""
    drawing_numbers = []
    for page_number in range(num_of_pages):
        with pdfplumber.open(filename) as pdf:
            page = pdf.pages[page_number]
            area = page.within_bbox((1000, 650, 1190, 800))
            text = area.extract_text()
            search_string = re.compile(r'.*' + drawing_number_element + '.*')
            try:
                drawing_number = re.search(search_string, text).group()
                print(f'\tPage {page_number + 1} of '
                      f'{num_of_pages}: {drawing_number}')
                drawing_numbers.append(drawing_number)
            except (TypeError, AttributeError):
                print(f'\tPage {page_number + 1} of '
                      f'{num_of_pages}: invalid drawing')
    return drawing_numbers


def save_drawings(filename, num_of_pages, drawing_numbers):
    """Saves each page of a PDF as a single page PDF file, named after
    the drawing number."""
    with open(filename, 'rb') as pdf:
        if len(drawing_numbers):
            warnings.filterwarnings('ignore')
            pdfReader = PyPDF2.PdfFileReader(pdf, strict=False)
            for page_number in range(num_of_pages):
                pdfWriter = PyPDF2.PdfFileWriter()
                pageObj = pdfReader.getPage(page_number)
                pdfWriter.addPage(pageObj)
                pdfOutputFile = open(drawing_numbers[page_number]
                                     + '.pdf', 'wb')
                pdfWriter.write(pdfOutputFile)
                pdfOutputFile.close()
            print(f'Drawings saved: {len(drawing_numbers)}')
        else:
            print('No drawings could be saved.')
    warnings.filterwarnings('default')


def get_filenames(directory=os.getcwd()):
    """Return a list of all the pdf files in a given directory."""
    pdf_files = []
    for filename in os.listdir(directory):
        if filename.endswith('.pdf'):
            pdf_files.append(os.path.join(directory, filename))
    return pdf_files


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('Usage: python drawing_splitter.py dwg-number-element')
        sys.exit()
    drawing_number_element = sys.argv[1]
    pdf_files = get_filenames()
    print('Drawing Splitter\n')
    print(f'Total files to process: {len(pdf_files)}')
    print(f'Using drawing number element: {drawing_number_element}\n')
    for filename in pdf_files:
        print(f'Processing file: {os.path.basename(filename)}...')
        num_of_pages = get_pdf_length(filename)
        drawing_numbers = get_drawing_numbers(filename, num_of_pages,
                                              drawing_number_element)
        save_drawings(filename, num_of_pages, drawing_numbers)
        print()
    print(f'Finished processing {len(pdf_files)} files.')
