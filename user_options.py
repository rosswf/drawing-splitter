import argparse

parser = argparse.ArgumentParser(description="""A tool for splitting combined
                                             drawing PDFs into seperate files
                                             named by drawing number.""")
parser.add_argument('dwg_number_element',
                    metavar='dwg-number-element',
                    type=str,
                    help='The part of the drawing number to be searched for')
parser.add_argument('-i',
                    '--input',
                    metavar='FOLDER',
                    type=str,
                    help='Folder where the PDF files are located',
                    default='.')
parser.add_argument('-o',
                    '--output',
                    metavar='FOLDER',
                    type=str,
                    help='Folder to save the PDF files in',
                    default='.')
