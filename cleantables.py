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

Function Summaries
batch_pdf2csv(pdfs) converts a list of PDFs into CSVs
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
    **Update: This function is not necessary, as tabula-py natively has
              support for batch processing of PDFs.
    
    Will convert input files into a comma-separated values (CSV) text
    file.
    
    Function:
    Asserts that the input is a list of file names (string) that can be
    used to access actual files. Then converts the PDF file names into
    CSV file names by concatenating the '.csv' extension. Asserts that
    these new file names are not shared with anything in the current
    directory.
    
    :param pdfs: list of strings, names of PDFs to be translated
    :return: list of strings, names of CSVs generated
    '''
    assert isinstance(pdfs, list), "Input must be a list."
    for name in pdfs:
        assert isinstance(name, str), "File names must be str"
        #Every element in pdfs should be a string
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
    
    for file in pdfs:
        tb.convert_into(file, newfiles[file], output_format='csv')
        #Convert file into CSV called file.csv
    
    return newfiles


def find_UCSDpoliceLog_URLs(startDate, endDate, urlform):
    '''
    Generate the URLs for the posted UCSD daily police log in a given
    time period. Logs are taken down within a period of one month, so
    there will be a cap of 30 days between the start and end dates.
    
    :param startDate: str, first log date in mmddyyyy format
    :param endDate: str, last log date in mmddyyyy format
    :param urlform: str, format of the URL with marked date locations
    :return: list of str, URLs of the specified daily police logs
    '''
    
    assert isinstance(startDate, str), \
           "Starting date must be a str type variable"
    assert isinstance(endDate, str), \
           "Ending date must be a str type variable"
    assert len(startDate) == 8, \
           "Starting date must be in mmddyyyy format"
    assert len(endDate) == 8, \
           "Ending date must be in mmddyyyy format"
    assert isinstance(urlform, str)
    
    import numpy
    
    return None


def batch_clean_tab_csv(
        csvs,
        heads,
        hrow=3, #default for tabula raws of the CJSC data
        splitcol=range(1,10), #default for CA 1952-1996 data
        by_year=range(2013,2018) #default is range of SD crime data
        ):
    '''
    Clean CSV output from tabula output by file name.
    
    :param csvs: list of str, file locations of CSVs to be cleaned
    :param heads: list of str, header labels; ignored if empty
    :param hrow: int, index of header row
    :param splitcol: list of int >=0, indices of column to be split
    :param by_year: tuple, specifies which year each CSV covers
    :return: pandas DataFrame; cleaned & combined data from CSVs
    '''
    from os import path
    import pandas as pd
    import numpy as np
    from string import split
    
    #Checking the list of CSVs input
    assert isinstance(csvs, list), 'Provide file locations as a list'
    assert len(csvs) > 0, 'CSV list cannot be empty'
    #This would cause an error when trying to concatenate nothing
    for item in csvs:
        assert isinstance(item, str), 'File name must be a string'
        assert path.exists(item), \
               '%s not found in directory' % (item)
    
    #checking the new header names input
    assert len(heads) == len( set(heads) ), \
           "Column headers must be unique"
    
    #Checking the input for the row where the data starts
    assert isinstance(hrow, int), 'Header row count must be int'
    
    #Checking the input for identifying improperly split columns
    assert isinstance(splitcol, list), \
           'Columns to split must be in a list'
    if len(splitcol) != 0:
        for id in splitcol:
            assert isinstance(id, int), \
                   "Column to split must be identified by integer index"
            assert id >= 0, \
                   "Column integer must be >= 0."
    assert len(splitcol) == len( set(splitcol) ), \
           "Unique indices required to specify which columns to split"
         
    #Checking the input for when the year is in the title, not the table
    assert isinstance(by_year, list), \
           "Years for the tables must be in a list."
    if len(by_year) > 0: #if the list of years is not empty
        assert len(by_year) >= len(csvs), \
               "Not every CSV listed has been assigned a year"
        for year in by_year:
            assert isinstance(year, int), "Years must be type int"
    
    def split_columns(inFrame, splitcol):
        '''
        Splits up specified data in a dataframe while preserving
        original column order.
        
        :param indata: pandas DataFrame, frame to be split up
        :param splitcol: list, column indices that need to be split
        :return: pandas DataFrame, new frame with split-up columns
        '''
        inFrame.columns = range( len(rawFrame.columns) )
        #labeling columns by index to easier specify what to exclude
        splitter = lambda pair: pd.series( [i for i in split(pair)] )
        #subfunction that does the actual job of splitting cells
        for index in splitcol:
            inFrame = inFrame[index].apply(splitter)
            #splits the dataframe at each specified axis
        return inFrame
            
    allFrames = [] #list to store dataframes
    
    #Going into each CSV, pulling out a dataframe, and cleaning it
    for csv in csvs:
        rawFrame = pd.read_csv(csv, header=hrow)
        #Convert the CSV into a dataframe
        rawFrame = rawFrame.dropna(how='all', axis=1)
        #Removing all empty columns which only contian NaN
        rawFrame = rawFrame.dropna(how='any', axis=0)
        #Removes possible extra header rows from tabula output
        
        if len(splitcol) != 0: #if some columns need splitting
            splitcol.sort() #lines up indices in order
            assert len(rawFrame.columns) < splitcol[-1], \
                   "Column %d is outside of table range" \
                   % (splitcol[-1])
            #Checks that columns to split are within range
            #Column indices refer to the table w/o NaN-only columns
            rawFrame = split_columns(rawFrame)
            #Split up columns that contain multiple pieces of data
        else:
            pass #Do nothing if splitcol is an empty list (default)
        
        allFrames.append(rawFrame)
        #Once the dataframe is processed, add to the list of frames
    
    #Ensuring that the inputs match before concatenation
    for frame in allFrames:
        assert frame.shape[1] == allFrames[0].shape[1], \
               "Not all inputs have the same column number"
               #Compare column counts to the first dataframe in list
        assert frame.shape[1] == len(heads), \
               "Total headings given must match dataframe's %d cols" \
               % (frame.shape[1])
               #Needs same number of headings as columns
        frame.columns = heads
        #Give each dataframe matching columns before concatenation
    
    if len(by_year) > 0: #If years are manually provided
        outdata = pd.concat(
                  allFrames,
                  axis=0,
                  keys=by_year,
                  names=['year','row']
                  )
                  #Adds a second index that tracks the data by year
    else:
        outdata = pd.concat(allFrames, axis=0)
    #combine all of the frames into one dataframe either way
    
    return outdata #will want to pickle this, but this works for now



def split_columns(inFrame, splitcol, heads=[]):
    '''
    Splits up specified data in a dataframe while preserving
    original column order.
    
    First, split_columns() asserts that parameters are of the required
    datatypes. Note that attempting to split anything not string will
    not work, and the list of columns to split must be of non-zero
    length.
    
    Then reassigns column headers such that each column may be referred
    to by order index, >= 0. Asserts that each of the requested columns
    fall within the column index range.
    
    Next, the output DataFrame receives its first column. Will split
    the column if index 0 is included or just assign if not. Goes on to
    loop through remaining column indices, splitting and expanding each
    column listed in splitcol. Anything not listed is just tacked on
    otherwise.
    
    The default is to re-assign numerical indices for the header, but if
    a list is provided, will assert that the list fits the DataFrame
    before assigning the new column headers. Then returns the split-up
    DataFrame.
    
    :param inFrame: pandas DataFrame, frame to be split up
    :param splitcol: list, len>0, indices of columns to be split
    :param heads: list of str, new headers, number indices otherwise
    :return: pandas DataFrame, new frame with split-up columns
    '''
    import pandas as pd
    import numpy as np
    
    #Check the DataFrame input
    assert isinstance(inFrame, pd.DataFrame), \
           "Input DataFrame must be a pandas DataFrame."
    
    #Check the list of columns to split
    assert isinstance(splitcol, list), \
           "Columns to split must be in a list."
    assert len(splitcol) > 0, "List of columns is empty."
    for id in splitcol:
        assert isinstance(id, int), \
               "Column to split must be identified by integer index"
        assert id >= 0, "Column integer must be >= 0."
    
    #Check the list of headings
    assert isinstance(heads, list), "Heading inputs must be in a list."
    for h in heads:
        assert isinstance(h, (str,int)), \
               "Headings in list must be strings or integers."
    
    inFrame.columns = range( len(inFrame.columns) )
    #labeling columns by index to easier specify what to exclude
    splitcol.sort()
    #Put columns in increasing order so output matches inFrame's order
    assert splitcol[-1] <= inFrame.columns[-1], \
           "%d is not in range of the input frame columns." \
           % (splitcol[-1])
           #Make sure that all of the desired splits will work
    for ind in splitcol:
        assert isinstance(inFrame[ind], object), \
               "Values in column %d must be object types" % (ind)
        #.str.split() will only accept object type inputs
    
    #Starting the output DataFrame, splitFrame
    if 0 in splitcol:
        splitFrame = inFrame[0].str.split(expand=True)
        #Splits first column if listed in splitcol
        #Note: Series.str.split() doesn't change original Series
    else:
        splitFrame = inFrame[0]
        #Just put in first column it won't split
    
    for col in inFrame.columns:
        #going through each column from input
        if col == 0:
            pass #Index 0 already handled; don't do anything
        elif col in splitcol:
            newsplit = inFrame[col].str.split(expand=True)
            splitFrame = pd.concat([splitFrame, newsplit], axis = 1)
            #Put in the newly split column; indices should match already
        else:
            splitFrame = pd.concat([splitFrame, inFrame[col]], axis = 1)
            #Columns that don't need splitting are just added on
    
    if len(heads) != 0: #adds headers if provided
        assert len(heads) == len( splitFrame.columns ), \
               "Heading list provided does not match DataFrame output."
        #Making sure that the heasders match the output shape
        splitFrame.columns = heads
        #assign headers to the output DataFrame
    else:
        splitFrame.columns = range( len(splitFrame.columns) )
        #default assigns headers by counting numerical indices
    
    assert bool( splitFrame.index.all() == inFrame.index.all() ), \
           "Output indices do not match the input."
    #Make sure nothing happened to the row indices
    
    #Return the new dataframe with split-up columns
    return splitFrame