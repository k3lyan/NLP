# Microsoft support files extraction
This module aims at extracting all type of microsoft office support files to raw text files. Apache tika is used for that.

# APACHE TIKA ALLOWS TO EXTRACT PDF XLS PPT DOCX 
## Requirements
* Download Apache Tika here
* Download Java ImageIO plugin for JBIG2 here (Source Code)
* Download JAI Image I/O Tools Core
* Download JPEG2000 support for Java Advanced Imaging Image I/O Tools API core from bintray
* Install tika-python:
`$pip3 install tika`

## Getting Started
Start the Apache Tika server and make sure that the jar files are in the classpath. For example:
`$java -cp "./*" org.apache.tika.server.TikaServerCli`     
will start the server at 9998 (default port) with the above mentioned jar files in the current directory.     


