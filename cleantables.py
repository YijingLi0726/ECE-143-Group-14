'''
crimepdf.py is a module with the purpose of scraping data out of PDF
files published in sandag.org which contain tables of crime statistics
specified by year, city, type of crime, etc.

Will rely on already-published module pdf2txt.py available as part of
the tabula-py package ( https://github.com/chezou/tabula-py ). As its
name suggests, the module will convert the pdf files to text.

Once we have text files, we can parse the data and look for the patterns
that make up tables in the original file. Ultimately, we want to store
this data as numpy arrays or pandas tables to make them amenable to
visual analysis via matplotlib.

Modules required:   tabula-py, os
'''

try:
    import tabula
except:
    print "tabula-py not installed. " \
          + "Go to https://github.com/chezou/tabula-py"

import tabula as tb
import os

def batch_pdf2csv(pdfs):
    '''
    Will convert input files into a comma-separated values (CSV) text
    file.
    
    Function:
    Asserts that the input is a list of file names (string) that can be
    used to access actual files. Then converts the PDF file names into
    CSV file names by concatenating the '.csv' extension. Asserts that
    these new file names are not shared with anything in the current
    directory.
    
    :param fnames: list of strings, names of PDFs to be translated
    :return: list of strings, names of CSVs generated
    '''
    assert isinstance(pdfs, list), "Input must be a list."
    for name in pdfs:
        assert isinstance(name, str), "File names must be str"
        #Every element in fnames should be a string
        assert os.path.exists(name), "File %s not found" % name
        #Every string should lead to an actual file
    
    newfiles = {} #Dictionary of old files with new names
    for ori in pdfs: #go through ORIginal file names
        newfiles[ori] = ori + ".csv" #adds .csv file extension
    #newfiles now has all of the names of the output files
    #This means that the new files will be in same dir as originals
    for new in newfiles:
        assert not os.path.exists(newfiles[new]), \
               "%s file already exists" % (newfiles[new])
        #avoid deleting/changing files already made
    
    for i, file in enumerate(fnames):
        tb.convert_into(file, newfiles[i], output_format='csv')
        #Convert file into CSV called file.csv
    
    return newfiles
        