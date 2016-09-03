import MSExtract as mse
import numpy as np



### CONSTRUCT TEST DATA

# make a params list to test with
#    mz_min   mz_max   dt_min  dt_max  rt_min   rt_max
p = [123.456, 234.567, 34,     45,     56,       67]

### DEFINE TESTS

def test_get_ms_name():
	print "testing get_ms_name()..."
	# test list of raw file names in different formats to make sure that the .raw is clipped off 
	# as it should be and the MS file is named correctly
	rfn = ["raw00000001.raw", "raw.number.one.raw", ".hidden-raw-file.raw", "00239120390.raw"]
	# list of the correct resulting ms file names
	cfn = ["raw00000001_123-234_34-45_56-67_MS.txt", "raw.number.one_123-234_34-45_56-67_MS.txt",\
			".hidden-raw-file_123-234_34-45_56-67_MS.txt", "00239120390_123-234_34-45_56-67_MS.txt"]
	for n in range(len(rfn)):
		if not mse.get_ms_name(p, rfn[n]) == cfn[n]:
			raise ValueError("name was not generated correctly from " + rfn[n])
	print "...PASS"

def test_match_data_shape():
	print "testing match_data_shape()..."
	# test with two arrays both with a single column, first array is longer
	a = np.array([[0,1,2,3,4,5,6,7,8]])
	b = np.array([[6,7,8]])
	a,b = mse.match_data_shape(a, b)
	if not a.shape[1] == b.shape[1]:
		raise ValueError("match_data_shape(a,b) failed!")
	# test with two arrays both with a single column, second array is longer
	c = np.array([[6,7,8]])
	d = np.array([[0,1,2,3,4,5,6,7,8]])
	c,d = mse.match_data_shape(c, d)
	if not c.shape[1] == d.shape[1]:
		raise ValueError("match_data_shape(c,d) failed")
	# test with two arrays both with two columns, first array is longer
	e = np.array([[0,1,2,3,4,5,6,7,8],[10,11,12,13,14,15,16,17,18]])
	f = np.array([[6,7,8], [9,10,11]])
	e,f = mse.match_data_shape(e, f)
	if not e.shape[1] == f.shape[1]:
		raise ValueError("match_data_shape(e,f) failed")
	# test with two arrays both with two columns, second array is longer
	g = np.array([[6,7,8], [9,10,11]])
	h = np.array([[0,1,2,3,4,5,6,7,8],[10,11,12,13,14,15,16,17,18]])
	g,h = mse.match_data_shape(g, h)
	if not g.shape[1] == h.shape[1]:
		raise ValueError("match_data_shape(g,h) failed")
	print "...PASS"

def test_comb_param_set_data():
	# construct three data files to be stand-ins for CDCReader output files, all different lengths
	# with different numbers
	a = np.arange(0)
	

### RUN TESTS

test_get_ms_name()
test_match_data_shape()
test_comb_param_set_data()