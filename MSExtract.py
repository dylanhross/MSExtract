""" 
    MSExtract.py
    2016-09-02
    Mark Benhaim and Dylan Ross

    TODO: program description (synopsis of what it does, what inputs does it require, what
            outputs does it produce, any other requirements/dependencies)
"""
# import any necessary modules
import numpy 
from subprocess import call
import os
### os.remove("filename") to remove a file for cleanup


### DYLAN:  |
###         V
# cdcr_conv_rawfiles
#
#   loops through a list of raw files making calls to CDCReader using a parameter set
#
#   parameters:
#		param_set (list) -- list of parameters to use, in order: mz_min, mz_max, dt_min, dt_max
#                            rt_min, rt_max
#		raw_files (list) -- list of raw files to convert with CDCReader
#	returns:
#		ms_files (list) -- a list of CDCReader output MS.txt files generated using one parameter set
def cdcr_conv_rawfiles(param_set, raw_files):
    # create a list of MS files to eventually combine
    ms_files = []
    # loop through raw files
    for raw_file in raw_files:
    	ms_name = get_ms_name(raw_file)
        # call CDCReader on each raw file
        call(build_cdcr_call(param_set, raw_file, ms_name))
        # add the ms filename to the list of ms files
        ms_files.append(ms_name)
    # return the list of converted ms files
    return ms_files

# get_ms_name
#
#   creates a systematic name for the MS file converted from a raw file by CDCReader
#
#   parameters:
#		raw_file (string) -- name of the current raw file to convert
#	returns:
#		ms_filename (string) -- the name of the MS file
def get_ms_name(raw_file):
	

# comb_param_set_data
#
#   combines all of the extracted MS data files generated using a single parameter set into one file
#
#   parameters:
#		data_files (list) -- a list of CDCReader output MS.txt files generated using a single
#								parameter set 
#	returns:
#		none
def comb_param_set_data(data_files):
	

# build_cdcr_call
#
#   builds a function to CDCReader.exe using a parameter set and a .raw filename
#
#   parameters:
#       param_set (list) -- list of parameters to use, in order: mz_min, mz_max, dt_min, dt_max
#                            rt_min, rt_max
#       raw_file (string) -- the filename of the .raw file to convert
#		ms_filename (string) -- the file name of the MS file 
#       [path_to_cdcr (string)] -- path of the directory containing CDCReader.exe [optional, 
#                                   default = ".\\" (current working directory)]
#   returns:
#       call_line (string) -- the full function call to CDCReader    
def build_cdcr_call(param_set, raw_file, ms_filename, path_to_cdcr=".\\"):

### MARK: feel free to flesh this funciton out, I have included the code I have used in the past
###         for the same thing  |  
###                             V
"""
def buildFunctionCall(pathToCDCReader,\
                      pathToInputFile,\
                      outputPath,\
                      outputBaseName,\
                      imBin = 0.05):
    # build all the function call flags
    rFlagLine = "--raw_file '" + pathToInputFile + "' "
    mFlagLine = "--ms_file '" + outputPath + "MS_" + outputBaseName + ".txt' "
    iFlagLine = "--im_file '" + outputPath + "IM_" + outputBaseName + "_bin-" + str(imBin) + ".txt' "
    # do not perform any smoothing
    numberSmoothFlagLine = "--ms_number_smooth 0 "
    smoothWindowFlagLine = "--ms_smooth_window 0 "
    imBinFlagLine = "--im_bin " + str(imBin) + " "
   
   	MARK: I would probably make the --im_bin flag very large (like 5? or something) so that too much
   			time is not wasted creating it. Also, I think you might as well have the --ms_bin flag 
   			set to 0 for completely unbinned MS data
   
    # make the MS binning very large so that too much time isnt wasted creating it
    msBinFlagLine = "--ms_bin 10 "
    # call the function in powershell, via cmd
    callLine = "powershell " +\
               pathToCDCReader + " " +\
               rFlagLine + \
               mFlagLine + \
               iFlagLine + \
               numberSmoothFlagLine + \
               smoothWindowFlagLine + \
               imBinFlagLine + \
               msBinFlagLine
    # return the line containing the final function call
    return callLine
"""


# the main execution pathway
if __name__ == __main__:

    ### NOTE: anything that you want printed to the console during execution should go in
    ###         this section 

    ### MARK:    |
    ###          V
    ### TODO: parse command-line arguments, we need to eventually store the file names of
    ###         the two input files as strings in variables in this scope so that they can
    ###         be used for the import statement, I've created the variables with just 
    ###         empty strings for now. You can use sys.argv to get the arguments but I like
    ###         argparse since it takes care of all of the formatting and provides a nice
    ###         interface. It may also be worth while to add an an argument for the path to
    ###         the CDCReader executable so that this program can still be run outside of
    ###         the directory containing CDCReader
    param_set_list_filename = ""
    raw_file_list_filename = "" 

    # import data from input files
    param_sets = numpy.genfromtxt(param_set_list_filename, delimiter=',', unpack=True)
    raw_files = numpy.genfromtxt(raw_file_list_filename, dtype=str)

    ### TODO: loop through the list of parameter sets and: 
    ###         call a method that takes as a parameter the list of raw filenames and a 
    ###         single parameter set which then loops through that list of raw files, calls
    ###         a method that produces a calls to CDCReader using the parameter set and each
    ###         raw filename, finally returning a list of the relevant mass spectrum files 
    ###         (x_MS.txt). Then call a method that takes as a parameter a list of the relevant
    ###         data files, which imports all of the data, combines it, then outputs the final 
    ###         .csv file for that parameter set.
    # loop through parameter set list
    for n in range param_sets:
        comb_param_set_data(cdcr_conv_rawfiles(param_sets[:,n], raw_files))

    ### TODO: clean up all of the files we do not need anymore (the input files? any files 
    ###         generated by CDCReader)
    
    
    