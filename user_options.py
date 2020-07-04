import argparse
import toml

settings = toml.load('settings.toml')

parser = argparse.ArgumentParser(description="""A tool for splitting multi-page
                                             PDF drawings into seperate files
                                             named by drawing number.""")
parser.add_argument('dwg_number_element',
                    metavar='dwg-number-element',
                    type=str,
                    help='The part of the drawing number to be searched for',
                    nargs='?',
                    default=settings['dwg_number_element'])
parser.add_argument('-i',
                    '--input',
                    metavar='FOLDER',
                    type=str,
                    help="""Folder where the original PDF files are located
                         (DEFAULT: Current folder)""",
                    default=settings['input_folder'])
parser.add_argument('-o',
                    '--output',
                    metavar='FOLDER',
                    type=str,
                    help="""Folder to save the PDF files in
                         (DEFAULT: Current folder)""",
                    default=settings['output_folder'])
# If settings.toml is set to true, default needs to be true
if settings['delete']:
    parser.add_argument('-d',
                        '--delete',
                        help="""Delete original files after processing""",
                        action='store_false')
else:
    parser.add_argument('-d',
                        '--delete',
                        help="""Delete original files after processing""",
                        action='store_true')
# If settings.toml is set to true, default needs to be true
if settings['revision']:
    parser.add_argument('-r',
                        '--revision',
                        help="""Save drawings in folders by revision""",
                        action='store_false')
else:
    parser.add_argument('-r',
                        '--revision',
                        help="""Save drawings in folders by revision""",
                        action='store_true')

region_group = parser.add_mutually_exclusive_group()
region_group.add_argument('-p',
                          '--preset',
                          metavar='REGION',
                          type=str,
                          help="""Preset region of PDF containing drawing
                               number. Choose from: 'top-left', 'top-right',
                               'bot-left', 'bot-right', 'all'
                               (DEFAULT: bot-right)""",
                          default=settings['region'],
                          choices=['top-left', 'top-right', 'bot-left',
                                   'bot-right', 'all'])
region_group.add_argument('-c',
                          '--custom',
                          metavar=('x0', 'y0', 'x1', 'y1'),
                          type=int,
                          help="""Custom region of PDF containing drawing
                               number""",
                          nargs=4)
