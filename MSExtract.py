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
    program_description = "This program performs .raw to .txt conversion of all .raw files in \
                  a specified directory using CDCReader.exe"
    # initialize an ArgumentParser with the program description
    parser = argparse.ArgumentParser(description=program_description) 
    # add arguments to the parser
    parser.add_argument('--CDCR',\
                        required=True,\
                        help='full path to CDCReader.exe',\
                        dest='path_to_cdcr',\
                        metavar='/full/path/to/CDCReader.exe')
    parser.add_argument('-pl', '--param-set-list',\
    			        required=True,\
    			        help='File containing parameter set list',\
    			        dest='param_set_list_filename',\
    			        metavar='/full/path/to/param_set_list.csv')
    parser.add_argument('-rl', '--raw-file-list',\
    			        required=True,\
    			        help='Plain text list containing HDX .raw file names',\
    			        dest='raw_file_list_filename',\
    			        metavar='/full/path/to/raw_file_list.txt')
    parser.add_argument('-c', '--clean-up',\
    			        required=False,\
    			        help='Clean up unecessary files after completion',\
    			        dest='clean',\
    			        action='store_true')
    parser.add_argument('-v', '--verbose',\
    			        required=False,\
    			        help='Be loud and noisy',\
    			        dest='verbose',\
    			        action='store_true')			
    return parser


# build_cdcr_call
#
#   builds a function to CDCReader.exe using a parameter set and a .raw filename
#
#   parameters:
#		param_set (list) -- list of parameters to use, in order: pep_mz, z, mz_min, mz_max, rt_min, 
#                           rt_max, dt_min, dt_max
#       raw_file (string) -- the filename of the .raw file to convert
#		ms_file (string) -- the file name of the MS file 
#       path_to_cdcr (string) -- path of the directory containing CDCReader.exe 
#   returns:
#       call_line (string) -- the full function call to CDCReader    
def build_cdcr_call(param_set, raw_file, ms_file, path_to_cdcr):
    # build all the function call flags
    r_flag = "--raw_file '" + raw_file + "' "
    m_flag = "--ms_file '" + ms_file + "' "
    i_flag = "--im_file 'IM.txt' "
    ms_start_flag = "--mass_start " + str(param_set[2]) + " "
    ms_end_flag = "--mass_end " + str(param_set[3]) + " "
    rt_scan_start_flag = "--scan_start " + str(int(round(param_set[4]))) + " "
    rt_scan_end_flag = "--scan_end " + str(int(round(param_set[5]))) + " "
    dt_scan_start_flag = "--dt_scan_start " + str(int(round(param_set[6]))) + " "
    dt_scan_end_flag = "--dt_scan_end " + str(int(round(param_set[7]))) + " "
    # do not perform any smoothing
    numberSmoothFlagLine = "--ms_number_smooth 0 "
    smoothWindowFlagLine = "--ms_smooth_window 0 "
    imBinFlagLine = "--im_bin 10 "
    # CDCReader Default setting is to average intensity values when binning, here we have set it to sum the values
    binSumFlagLine = "--bin_sum 1 "
    msBinFlagLine = "--ms_bin 0 "
    # call_line corresponds to function call, via cmd
    call_line = "powershell " +\
               path_to_cdcr + " " +\
               r_flag + \
               m_flag + \
               i_flag + \
               numberSmoothFlagLine + \
               smoothWindowFlagLine + \
               imBinFlagLine + \
               msBinFlagLine + \
               ms_start_flag + \
               ms_end_flag + \
               rt_scan_start_flag + \
               rt_scan_end_flag + \
               dt_scan_start_flag + \
               dt_scan_end_flag 
    # return the line containing the final function call
    return call_line


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
    param_str = ""
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

# get_cal_numbers
#
#   looks in a raw file's _HEADER.txt file for the mass calibration parameters
#
#   parameters:
#		filename (string) -- the name of the .raw file to look for calibration parameters in the 
#                               header file
#		[cal_line (int)] -- the line in the xxxx.raw/_HEADER.txt file containing the calibration
#                           numbers [optional, default=51] 
#	returns:
#		numbers (list) -- a list of all the numbers found in the specified line of the header file
def get_cal_numbers(filename, cal_line=52):
    with open(filename + "/_HEADER.txt", "r") as input:
        cal_string = input.readlines()[cal_line - 1]
        if not cal_string.startswith('$$ Cal Function'):
            raise ValueError('line ' + str(cal_line) + ' of '+ filename + '/_HEADER.txt did' + \
                    ' not contian "$$ Cal Function"... please check the contents of that file')
        # regex for matching numbers in exponential notation (e.g. -123.456e7 or 123.456e-7)
        # '[-]*\d+[.]\d+[e][-]*\d+'
        # return the list converted into floats
        return [float(i) for i in re.findall('[-]*\d+[.]\d+[e][-]*\d+', cal_string)]


# correct_mz
#
#   corrects an mz value using mass calibration parameters from the _HEADER.txt file
#
#   parameters:
#		cal_numbers (list) -- a list of all mass calibration numbers from the _HEADER.txt file
#       mz (float) -- the m/z to correct
#	returns:
#		corrected_mz (float) -- the corrected m/z value
def correct_mz(cal_numbers, mz):
    sqrt_mz = numpy.sqrt(mz)
    sqrt_mz = cal_numbers[0] + sqrt_mz * \
            (cal_numbers[1] + sqrt_mz * \
            (cal_numbers[2] + sqrt_mz * \
            (cal_numbers[3] + sqrt_mz * \
            (cal_numbers[4] + sqrt_mz * \
            (cal_numbers[5])))))
    return sqrt_mz * sqrt_mz


# cdcr_conv_rawfiles
#
#   loops through a list of raw files making calls to CDCReader using a parameter set
#
#   parameters:
#		param_set (list) -- list of parameters to use, in order: pep_mz, z, mz_min, mz_max, rt_min, 
#                           rt_max, dt_min, dt_max
#		raw_files (list) -- list of raw files to convert with CDCReader
#       path_to_cdcr (string) -- full path to the CDCReader executable
#       [quiet (boolean)] -- don't print any information about what files are being converted 
#                               [default = True] 
#	returns:
#		ms_files (list) -- a list of CDCReader output MS.txt files generated using one parameter set
#                           and the raw file that each was generated from
def cdcr_conv_rawfiles(param_set, raw_files, path_to_cdcr, quiet=True):
    # create a list of MS files to eventually combine
    ms_files = []
    # loop through raw files
    for raw_file in raw_files:
    	ms_name = get_ms_name(param_set, raw_file)
        # verbose option
        if not quiet:
            print "Now converting " + raw_file + " using parameter set " + get_param_str(param_set) + "..."
        # call CDCReader on each raw file
        call(build_cdcr_call(param_set, raw_file, ms_name, path_to_cdcr))
        # verbose option
        if not quiet:
            print "...DONE"
        # add the ms filename and the raw filename to the list of ms files
        ms_files.append([ms_name, raw_file])
    # return the list of converted ms files
    return ms_files


# comb_param_set_data
#
#   combines all of the extracted MS data files generated using a single parameter set into one .csv
#	file named using the formula: "pepmz_z.csv". Also corrects mz values using the mass calibration 
#   parameters in the _HEADER.txt file inside the .raw file
#
#   parameters:
#		data_files (list) -- a list of CDCReader output MS.txt files generated using a single
#								parameter set and the raw files they were generated from
#		param_set (list) -- list of parameters to use, in order: pep_mz, z, mz_min, mz_max, rt_min, 
#                           rt_max, dt_min, dt_max
#	returns:
#		none
def comb_param_set_data(data_files, param_set):
    # create a master data array starting with the first MS data file
    master_data = numpy.genfromtxt(data_files[0][0], unpack=True)
    # correct the first set of mz values
    master_data[0] = correct_mz(get_cal_numbers(data_files[0][1]), master_data[0])
    # loop through data_files and import their data
    for n in range(1, len(data_files)):
        # import the next data set
        add_data = numpy.genfromtxt(data_files[n][0], unpack=True)
        # correct mz values in add_data
        master_data[0] = correct_mz(get_cal_numbers(data_files[n][1]), master_data[0])
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
    # looks for:
    #    *anything*_*number*-*number*_*number*-*number*_*number*-*number*_MS.txt
    pattern = re.compile('.*_(\d+-\d+_){3}MS\.txt$')
    # search through all of the files in the current working directory and remove ones that match the 
    # regular expression for the MS.txt files
    for name in os.listdir('.'):
        if pattern.match(name):
            os.remove(name)
    # remove IM.txt
    os.remove("IM.txt")


# main execution pathway (invoked when program is called directly)
if __name__ == "__main__":

    ### NOTE: anything that you want printed to the console during execution should go in
    ###         this section 

    # create an argument parser and get the command line arguments
    print
    args = prep_parser().parse_args()
    # import data from input files
    param_sets = numpy.genfromtxt(args.param_set_list_filename, delimiter=',', unpack=True)
    raw_files = numpy.genfromtxt(args.raw_file_list_filename, dtype=str)
    # loop through parameter set list and perform file conversion and data combination for each 
    # parameter set
    for n in range(len(param_sets[0,:])):
        comb_param_set_data(cdcr_conv_rawfiles(param_sets[:,n], raw_files, args.path_to_cdcr, quiet=(not args.verbose)), param_sets[:,n])
    # if clean-up flag has been set, remove any unneeded files from the working directory
    if args.clean:
    	clean_up()