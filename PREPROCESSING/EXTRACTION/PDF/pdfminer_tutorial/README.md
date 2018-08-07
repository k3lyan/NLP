# Extract Text
A module to extract raw text from any document format (PDF, Microsoft Office etc.)

## Requirements
Download Apache Tika [here](https://tika.apache.org/download.html "Download Link for Apache Tika")

Download Java ImageIO plugin for JBIG2 [here](http://search.maven.org/#search%7Cga%7C1%7Clevigo-jbig2-imageio) ([Source Code](https://github.com/levigo/jbig2-imageio/tree/levigo-jbig2-imageio-2.0))

Download [JAI Image I/O Tools Core](https://github.com/jai-imageio/jai-imageio-core/releases)

Download [JPEG2000 support](https://github.com/jai-imageio/jai-imageio-jpeg2000) for Java Advanced Imaging Image I/O Tools API core from [bintray](https://bintray.com/jai-imageio/maven/jai-imageio-jpeg2000#files/com/github/jai-imageio/jai-imageio-jpeg2000/1.3.0)

Install tika-python ([Source Code](https://github.com/chrismattmann/tika-python))

`pip install tika`

## Getting Started
Start the Apache Tika server and make sure that the jar files are in the classpath. For example,

`java -cp "./*" org.apache.tika.server.TikaServerCli`

will start the server at 9998 (default port) with the above mentioned jar files in the current directory.

# Extract PDFs to texts

## Extract text from PDF (fine-grained extraction)
The wrapper_pdf.py python script builds a class PdfMinerWrapper which parses the pdf file put in input into LTPage objects (one for each page). An LTPage object which may contain child objects like LTTextBox, LTFigure, LTImage, etc.
Loop on the pages: 
  * Each LTPage object might contains several LTTextBox objects: 
  * Each LTTextBox might contains box objects  
  * Each box object (generally corresponding to a line in the initial pdf document) contains: 
    * the full string (the sentence) 
    * the positions of the box (which contains the line-sentence in the pdf file) 
    * characters objects (LTChar object)
  * Each LTChar object (corresponding to the different characters in the sentence) contains:
    * the character
    * the font used for this character ('Bold' is added when the character is bold)
    * the font size

## wrapper_pdf.py: analyzer and parser
Methods used: PDFParser, PDFPage, PDFDocument, PDFResourceManager, PDFPageInterpreter, PDFPageAggregator, LAParams
 * Open the pdf file with python: 
      file = open(path_pdf, 'rb')
 * Create a parser object associated with the file: 
      parser = pdfminer.parser(file)  
 * Create a PDF Document object that stores the document structure, set the password to "": 
      doc = pdfminer.pdfdocument(parser, password="") 
 * Connect the parser and the document object:
      parser.set_document(doc)
 * Create a resource manager: 
      rsrcmgr = PDFResourceManager()
 * Set your exploring parameters: 
      laparams = LAParams(char_margin=3.5, all_texts = True)
 * Connect the resource manager to these settled parameters by creating the exploring device: 
      device = PDFPageAggregator(rsrcmgr, laparams=laparams)
 * Create a page interpreter:
      interpreter = PDFPageInterpreter(rsrcmgr, device)
 * For each page of the doc: process the page with the interpreter and get the LTPage object of this page, giving you a lot of information about the text in the page (font style, font size, positions of the blocks,...etc)

## extractor_pdf.py: extractor
Methods used: PDFPage, LTTextBox, LTChar, LTFigure
The extractor_pdf.py python script allows you, by analyzing the LTPage objects created by wrapper_pdf.py, to convert a pdf file into text documents, at different scale levels: 
 * all the pages 
 * a sequence of pages 
 * a sequence of sentences in a targeted page 
 * a sequence of words in a targeted sentence
 * the features of a specific word (font size and style) 
The selection of the extracting scale precision is made through a questions/answers process to the client using the script.
A new directory is then created containing the text file produced by the script.

## Getting Started
Make sure your pdf file is in the same directory than your python scripts. Then run on the same folder:
* $ python extractor_pdf.py my_pdf_file.pdf 

## Convert each paragraphs of a pdf file into independant text files
The python script pdf2txt.py specifically aims at selecting and extracting subparts (from one subtitle to the next one) of the pdf. It create a new text file for every ot these subparts, getting the title of the subpart as a file name. To "detect" the subtitles of the pdf, the selection process is the following one:
Look at each LTTextBox (reach the LTChar level) if:
* the size is higher than a specified threshold
* all the character (LTChar level) has a bold font
* the first character is a number

## Getting Started
Make sure your pdf file(s) are in the same directory than your scripts.
* For one pdf: $ python pdf2txt.py my_pdf_file.pdf
* For several pdf files: $./pdf2txt.sh
