# Drawing Splitter

A tool for splitting combined drawing PDFs into single files named by drawing number.

## Setup

Install the required packages from requirements.txt

```bash
pip install -r requirements.txt
```

## Usage

```bash
python3 drawing_splitter.py dwg-number-element
```

Where dwg-number-element is a part of the drawing number to be searched for within the drawing, this should be common between all drawings sheets. 
If following BS EN ISO 19650, Project Number or Originator are suggested.

## Notes

- For now, only PDF files located in the same directory as the program are processed. The seperated PDFs will also be saved in this same directory.
- For now, only drawing numbers located in the bottom right hand corner of an A3 size PDF can be read.
- For now, all drawings will be processed with the same dwg-number-element.
- Text extraction can be quite slow depending on the PDF.

## Roadmap

Add optional command-line arguments for the following:
- Specify a directory that the PDF files are located in.
- Specify a directory to save the split PDF files.
- Specify a region of the PDF where the drawing number can be located.

## Contributions

This is my first python project so pull requests & feedback are more than welcome.

## Acknowledgements

Many thanks to:
- The contributors to PyPDF2
- The contributors to pdfplumber
