import MSExtract as mse

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
			print "...FAIL!"
			raise ValueError("name was not generated correctly from " + rfn[n])
	print "...PASS"


### RUN TESTS

test_get_ms_name()