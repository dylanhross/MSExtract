""" 
    MSExtract.py
    2016-09-02
    Mark Benhaim and Dylan Ross

    TODO: program description (synopsis of what it does, what inputs does it require, what
            outputs does it produce, any other requirements/dependencies)
"""
# import any necessary modules
from subprocess import call
import os
import re
import argparse
import numpy 


# prep_parser
#
#   prepares an argument parser object with all of the command-line flags that will be needed for
#	this program
#
#   parameters:
#       none
#   returns:
#       parser (ArgumentParser) -- an argument parser object
def prep_parser():
    
    ### NOTE: pass is just a placeholder, remove it when you add code here
	pass

### MARK: feel free to flesh this funciton out, I have included the code I have used in the past
###         for the same thing  |  
###                             V
"""
    program_description = "This program performs .raw to .txt conversion of all .raw files in \
                  a specified directory using CDCReader.exe"
    parser = argparse.ArgumentParser(description=program_description)
    
### program_description in the above parser line was written as programDescription which was not defined, changed it to program_description
    
    parser.add_argument('--data-dir',\
                        required=True,\
                        help='directory containing .raw files to convert',\
                        dest="dataDirectory",\
                        metavar='/full/path/to/data-dir/')
    parser.add_argument('--CDCR',\
                        required=True,\
                        help='full path to CDCReader.exe',\
                        dest="pathToCDCReader",\
                        metavar='/full/path/to/CDCReader.exe')
    parser.add_argument('--im-bin',\
                        required=False,\
                        help='value to bin masses by in IM-data.txt, default = 0.05',\
                        dest="imBin",\
                        default=0.05)
    parser.add_argument('--param_set_list','-p',\
    			required=True,\
    			help='File containing parameter set list',\
    			dest="param_set_list_filename",\
    			metavar='/full/path/to/folder_containing_paramsetlist.csv')
    parser.add_argument('--raw_file_list','-r',\
    			required=True,\
    			help='Plain text list containing HDX .raw file names',\
    			dest="raw_file_list_filename",\
    			metavar='/full/path/to/.raw/file.txt')
    parser.add_argument('--clean_up', '-c',\
    			required=False
    			help='Clean up unecessary files after completion',\
    			dest=clean_up,\
    			action='store_true')
    			
    #The cleanup is not required but when indicated is always true, I think that this works the way we are intending but I need to test it
    
    			
    return parser
    
    MARK: we need the following fields of the parser set correctly (i.e. the dest flag in each
    		add_argument method call):
    				1. param_set_list_filename -- filename of the parameter set list
    				2. raw_file_list_filename -- filename of the raw file list
    				3. clean_up -- must be set to True if -c/--clean-up is included, False otherwise
    					I am not sure exactly how to do that but im sure you can figure it out from
    					the documentation
    		you may also consider adding an (optional?) flag for specifying the location of the
    		CDCReader.exe executable, like the --CDCR flag above
"""



# build_cdcr_call
#
#   builds a function to CDCReader.exe using a parameter set and a .raw filename
#
#   parameters:
#		param_set (list) -- list of parameters to use, in order: pep_mz, z, mz_min, mz_max, rt_min, 
#                           rt_max, dt_min, dt_max
#       raw_file (string) -- the filename of the .raw file to convert
#		ms_filename (string) -- the file name of the MS file 
#       [path_to_cdcr (string)] -- path of the directory containing CDCReader.exe [optional, 
#                                   default = ".\\CDCReader.exe" (current working directory)]
#   returns:
#       call_line (string) -- the full function call to CDCReader    
def build_cdcr_call(param_set, raw_file, ms_filename, path_to_cdcr=".\\CDCReader.exe"):
	
	### NOTE: pass is just a placeholder, remove it when you add code here
	pass

### MARK: feel free to flesh this funciton out, I have included the code I have used in the past
###         for the same thing  |  
###                             V
"""
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
   			set to 0 for completely unbinned MS data. Also, if you set the --im_file flag to a 
   			constant value, it will be overwritten each time CDCReader is called, which would reduce
   			the buildup of junk files
   
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


# get_param_str
#
#   combines a parameter set into a single string using the formula: 
#	"mzmin-mzmax_rtmin-rtmax_dtmin-dtmax_" where all numerical values are integral (achieved by 
#	casting to int, decimals are rounded down)
#
#   parameters:
#		param_set (list) -- list of parameters to use, in order: pep_mz, z, mz_min, mz_max, rt_min, 
#                           rt_max, dt_min, dt_max
#	returns:
#		param_str (string) -- parameters collapsed into a string
def get_param_str(param_set):
	for n in range(2, len(param_set)):
		param_str += str(int(param_set[n]))
		if not n % 2:
			param_str += "-"
		else:
			param_str += "_"
	return param_str

# get_ms_name
#
#   creates a systematic name for the MS file converted from a raw file by CDCReader using the
#	formula: "raw-filename_mzmin-mzmax_dtmin-dtmax_rtmin-rtmax_MS.txt" where all numerical values
#	are integral (achieved by casting to int, decimals are rounded down)
#
#   parameters:
#		param_set (list) -- list of parameters to use, in order: pep_mz, z, mz_min, mz_max, rt_min, 
#                           rt_max, dt_min, dt_max
#		raw_file (string) -- name of the current raw file to convert
#	returns:
#		ms_filename (string) -- the name of the MS file
def get_ms_name(param_set, raw_file):
	# os.path.splitext removes .raw from the end of file name
	return os.path.splitext(raw_file)[0] + "_" + get_param_str(param_set) + "MS.txt"

# get_csv_name
#
#   creates a systematic name for the .csv output file using the formula: "pepmz_z.csv" where pepmz
#   is the peptide mz parameter with any decimal values represented with a p in place of the decimal 
#   point (e.g. 123.456 -> 123p456)
#
#   parameters:
#		param_set (list) -- list of parameters to use, in order: pep_mz, z, mz_min, mz_max, rt_min, 
#                           rt_max, dt_min, dt_max
#	returns:
#		csv_filename (string) -- the name of the MS file
def get_csv_name(param_set):
	return str(param_set[0]).replace(".", "p") + "_" + str(param_set[1]) + ".csv"

# match_data_shape
#
#   this method makes sure that the column lengths of two arrays are the same, such that one may be 
#	appended into the other. If the lengths are unequal, the array with the shorter column length
#	will be padded to the length of the other array by appending zeros to the ends of the columns
#	e.g. if two arrays have shapes (x, 5) and (y, 6) the first array will be padded so that it has
#	shape (x, 6). 
#
#   parameters:
#		array1 (numpy.ndarray) -- an array with shape (x, m)
#		array2 (numpy.ndarray) -- an array with shape (y, n)
#	returns:
#		array1, array2 (numpy.ndarray, numpy.ndarray) -- the (possibly modified) arrays
def match_data_shape(array1, array2):
	# store the array column lengths
	a1_len = array1.shape[1]
	a2_len = array2.shape[1]
	# compare column lengths using strictly less-than and strictly greater-than, if the lengths are 
	# equal, there is nothing to do
	if a1_len > a2_len:
		# pad array2 with zeros to the match the column length of array1
		array2 = numpy.pad(array2, ((0,0),(0,(a1_len - a2_len))), mode='constant')
	elif a2_len > a1_len:
		# pad array1 with zeros to the match the column length of array2
		array1 = numpy.pad(array1, ((0,0),(0,(a2_len - a1_len))), mode='constant')
	# need to return the two (possibly altered) arrays
	return array1, array2

# cdcr_conv_rawfiles
#
#   loops through a list of raw files making calls to CDCReader using a parameter set
#
#   parameters:
#		param_set (list) -- list of parameters to use, in order: pep_mz, z, mz_min, mz_max, rt_min, 
#                           rt_max, dt_min, dt_max
#		raw_files (list) -- list of raw files to convert with CDCReader
#	returns:
#		ms_files (list) -- a list of CDCReader output MS.txt files generated using one parameter set
def cdcr_conv_rawfiles(param_set, raw_files):
    # create a list of MS files to eventually combine
    ms_files = []
    # loop through raw files
    for raw_file in raw_files:
    	ms_name = get_ms_name(param_set, raw_file)
        # call CDCReader on each raw file
        call(build_cdcr_call(param_set, raw_file, ms_name))
        # add the ms filename to the list of ms files
        ms_files.append(ms_name)
    # return the list of converted ms files
    return ms_files


# comb_param_set_data
#
#   combines all of the extracted MS data files generated using a single parameter set into one .csv
#	file named using the formula: "pepmz_z.csv"
#
#   parameters:
#		data_files (list) -- a list of CDCReader output MS.txt files generated using a single
#								parameter set
#		param_set (list) -- list of parameters to use, in order: pep_mz, z, mz_min, mz_max, rt_min, 
#                           rt_max, dt_min, dt_max
#	returns:
#		none
def comb_param_set_data(data_files, param_set):
	# create a master data array starting with the first MS data file
	master_data = numpy.genfromtxt(data_files[0], unpack=True)
	# loop through data_files and import their data
	for n in range(1, len(data_files)):
		# import the next data set
		add_data = numpy.genfromtxt(data_files[n], unpack=True)
		# match the column lengths between master_data and add_data so they can be added together
		master_data,add_data = match_data_shape(master_data, add_data)
		# append add_data to master_data
		master_data = numpy.append(master_data, add_data, 0)
	# save combined data into a csv file
	numpy.savetxt((get_csv_name(param_set)), numpy.transpose(master_data), delimiter=",", fmt='%.6f')

# clean_up
#
#   removes any unneeded files from the current working directory, those being all files generated as 
#   outputs from CDCReader.exe: IM.txt + (all ...MS.txt files)
#
#   parameters:
#		none
#	returns:
#		none
def clean_up():
    # create a regular expression pattern to search for
    pattern = re.compile('_[\d+]-[\d+]_[\d+]-[\d+]_[\d+]-[\d+]_MS.txt$')
    # search through all of the files in the current working directory and remove ones that match the 
    # regular expression for the MS.txt files
    for name in os.listdir('.'):
        match = re.search(pattern, name)
        if match:
            print name, "would have been removed"
            #os.remove(name)

# main execution pathway (invoked when program is called directly)
if __name__ == "__main__":

    ### NOTE: anything that you want printed to the console during execution should go in
    ###         this section 
    
    # create an argument parser and get the command line arguments
    args = prep_parser().parse_args()
    
    # import data from input files
    param_sets = numpy.genfromtxt(args.param_set_list_filename, delimiter=',', unpack=True)
    raw_files = numpy.genfromtxt(args.raw_file_list_filename, dtype=str)

    # loop through parameter set list and perform file conversion and data combination for each 
    # parameter set
    for n in range(len(param_sets)):
        comb_param_set_data(cdcr_conv_rawfiles(param_sets[:,n], raw_files), param_sets[:,n])

    # if clean-up flag has been set, remove any unneeded files from the working directory
    if args.clean_up:
    	clean_up()

    
