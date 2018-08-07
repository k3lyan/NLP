# Microsoft support files extraction
This module aims at extracting all type of microsoft office support files to raw text files. Apache tika is used for that.

## Apache Tika 
### Requirements
* Download Apache Tika [here](https://tika.apache.org/download.html "Download Link for Apache Tika")
* Download Java ImageIO plugin for JBIG2 [here](http://search.maven.org/#search%7Cga%7C1%7Clevigo-jbig2-imageio) ([Source Code](https://github.com/levigo/jbig2-imageio/tree/levigo-jbig2-imageio-2.0))
* Download [JAI Image I/O Tools Core](https://github.com/jai-imageio/jai-imageio-core/releases)
* Download [JPEG2000 support](https://github.com/jai-imageio/jai-imageio-jpeg2000) for Java Advanced Imaging Image I/O Tools API core from [bintray](https://bintray.com/jai-imageio/maven/jai-imageio-jpeg2000#files/com/github/jai-imageio/jai-imageio-jpeg2000/1.3.0)
* Install tika-python ([Source Code](https://github.com/chrismattmann/tika-python)):    
`$pip3 install tika`

### Getting Started
Start the Apache Tika server and make sure that the jar files are in the classpath. For example:
`$java -cp "./*" org.apache.tika.server.TikaServerCli`     
will start the server at 9998 (default port) with the above mentioned jar files in the current directory.     


