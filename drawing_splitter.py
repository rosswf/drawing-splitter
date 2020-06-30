#!/usr/bin/env python3
"""A tool for splitting multi-page PDF drawings into seperate files named
by drawing number.

USAGE
    python3 drawing_splitter.py dwg-number-element

    Where dwg-number-element is a part of the drawing number to be
    searched for.

    See python3 drawing_splitter.py --help for full usage options.

"""
import re
import os
import warnings

import PyPDF2
import pdfplumber

import user_options


def get_pdf_length(filename):
    """Return the number of pages of a PDF given it's file name."""
    with pdfplumber.open(filename) as pdf:
        num_of_pages = len(pdf.pages)
        return num_of_pages


def get_drawing_numbers(filename, num_of_pages, number_element, region):
    """Return a list of drawing numbers, read from each page of a PDF."""
    drawing_numbers = []
    for page_number in range(num_of_pages):
        with pdfplumber.open(filename) as pdf:
            page = pdf.pages[page_number]
            area = page.within_bbox(region)
            text = area.extract_text()
            search_str = re.compile(r'[\w\d\-\(\)]*'
                                    + number_element
                                    + r'[\w\d\-\(\)]*')
            try:
                drawing_number = re.search(search_str, text).group()
                print(f'\tPage {page_number + 1} of '
                      f'{num_of_pages}: {drawing_number}')
                drawing_numbers.append(drawing_number)
            except (TypeError, AttributeError):
                print(f'\tPage {page_number + 1} of '
                      f'{num_of_pages}: Drawing number not found. '
                      'Manually rename file.')
                drawing_numbers.append(f'drawing_{page_number + 1}')
    return drawing_numbers


def save_drawings(filename, num_of_pages, drawing_numbers, output_folder):
    """Saves each page of a PDF as a single page PDF file, named after
    the drawing number."""
    warnings.filterwarnings('ignore')
    with open(filename, 'rb') as pdf:
        pdf_reader = PyPDF2.PdfFileReader(pdf, strict=False)
        for page_number in range(num_of_pages):
            pdf_writer = PyPDF2.PdfFileWriter()
            page = pdf_reader.getPage(page_number)
            pdf_writer.addPage(page)
            output_filename = drawing_numbers[page_number] + '.pdf'
            os.makedirs(output_folder, exist_ok=True)
            output_fullpath = os.path.join(output_folder, output_filename)
            pdf_output_file = open(output_fullpath, 'wb')
            pdf_writer.write(pdf_output_file)
            pdf_output_file.close()
        print(f'Drawings saved: {len(drawing_numbers)}')
    warnings.filterwarnings('default')


def get_filenames(directory):
    """Return a list of all the pdf files in a given directory."""
    if not os.path.isdir(directory):
        print(f'Folder {directory} does not exist.\n'
              'Using current directory instead.\n')
        directory = os.getcwd()
    pdf_files = []
    for filename in os.listdir(directory):
        if filename.endswith('.pdf'):
            pdf_files.append(os.path.join(directory, filename))
    return pdf_files


def get_page_size(filename):
    """Return the height and width of pages in the PDF, assumes all pages are
    the same size."""
    with pdfplumber.open(filename) as pdf:
        page_height = int(pdf.pages[0].height)
        page_width = int(pdf.pages[0].width)
    return (page_height, page_width)


def delete_file(filename):
    """Delete a file given its filename."""
    os.unlink(filename)
    print(f'Deleted file: {os.path.basename(filename)}')


if __name__ == '__main__':
    args = user_options.parser.parse_args()
    print('Drawing Splitter\n')
    number_element = args.dwg_number_element
    pdf_files = get_filenames(args.input)
    print(f'Total files to process: {len(pdf_files)}')
    print(f'Using drawing number element: {number_element}')
    print(f'Checking region: {args.preset}\n')
    for filename in pdf_files:
        page_size = get_page_size(filename)
        page_height = page_size[0]
        page_width = page_size[1]
        regions = {'top-left': (0, 0, page_width * 0.2, page_height * 0.5),
                   'top-right': (page_width * 0.8, 0,
                                 page_width, page_height * 0.5),
                   'bot-left': (0, page_height * 0.5, page_width * 0.2,
                                page_height),
                   'bot-right': (page_width * 0.8, page_height * 0.5,
                                 page_width, page_height),
                   'all': (0, 0, page_width, page_height)}
        print(f'Processing file: {os.path.basename(filename)}...')
        num_of_pages = get_pdf_length(filename)
        drawing_numbers = get_drawing_numbers(filename, num_of_pages,
                                              number_element,
                                              regions[args.preset])
        save_drawings(filename, num_of_pages, drawing_numbers, args.output)
        if args.delete:
            delete_file(filename)
        print()
    print(f'Finished processing {len(pdf_files)} files.')
