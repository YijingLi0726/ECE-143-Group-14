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


def batch_clean_tab_csv(
        csvs,
        heads,
        hrow=0,
        by_year=range(2013,2018) #default is range of SD crime data
        ):
    '''
    Clean CSV output from tabula output by file name. 
    Note: Will not generate output with NaN values.
    
    First asserts that all of the inputs are of the correct data type
    and format (see parameters below). Note that the default of hrow is
    0, so the first row will be used as the header row and all rows
    below it are considered data. The default range for the by_year data
    is 2013 to 2017, inclusive, due to the way the San Diego tables are
    organized. Note that this list must be empty for tables where the
    year is already in the data.
    
    Then it starts a list that takes in all of the processed dataFrames
    from directly reading the files.
    
    The function loops through each file path listed in the CSV list.
    Each CSV is read into a pandas file with the pandas.read_csv()
    function with hrow set as the header row index. The dataframe is
    trimmed of columns that are completely empty and then removes any
    rows containing a NaN, as these are mostly extra header rows.
    
    **If the output table should have some NaNs,
      DO NOT USE this function.
    
    Each trimmed DataFrame is stored in the list variable called
    earlier. The DataFrames in the list are then checked for matching
    number of columns, not column headers, since slight spacing
    differences across years can make a difference in row numbers.
    It is important that the format of each of the original CSVs do
    match exactly.
    
    If the headers were listed, then the new headers are assigned.
    Otherwise the function defaults to giving numerical indices going
    from 0 up to the right. The DataFrames are then concatenated,
    checked again for correct dimensions, then returned as output.
    
    :param csvs: list of str, file locations of CSVs to be cleaned
    :param heads: list of str, header labels; ignored if empty
    :param hrow: int, index of header row
    :param by_year: tuple, specifies which year each CSV covers
    :return: pandas DataFrame; cleaned & combined data from CSVs
    '''
    import pandas as pd
    import numpy as np
    
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
    
    #Checking the input for when the year is in the title, not the table
    assert isinstance(by_year, list), \
           "Years for the tables must be in a list."
    if len(by_year) > 0: #if the list of years is not empty
        assert len(by_year) >= len(csvs), \
               "Not every CSV listed has been assigned a year"
        for year in by_year:
            assert isinstance(year, int), "Years must be type int"
            
    allFrames = [] #list to store dataframes
    
    #Going into each CSV, pulling out a dataframe, and cleaning it
    for csv in csvs:
        rawFrame = pd.read_csv(csv, header=hrow)
        #Convert the CSV into a dataframe
        rawFrame = rawFrame.dropna(how='all', axis=1)
        #Removing all empty columns which only contian NaN
        rawFrame = rawFrame.dropna(how='any', axis=0)
        #Removes possible extra header rows from tabula output
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
    
    return outdata #will want to pickle this



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