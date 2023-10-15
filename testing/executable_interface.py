import os
import subprocess
import f90nml
from dataclasses import dataclass

def safe_mkdir(directory):
	"""
	
	Creates a directory with try expect
	
	"""
	try:
		if not os.path.exists(os.path.dirname(directory)):
			os.makedirs(os.path.dirname(directory))
	except OSError as err:
		print(err)

# Executable constants
mpiexec    = 'mpiexec'
exe_file   = "< name of executable >"
# Change name of directories appropriately
input_dir  = "./test_inputs/"
data_dir   = './test_data/'
output_dir = './test_outputs/'
safe_mkdir(output_dir)

@dataclass
class Test_CSVOutput:
	"""
	
	Dataclass for a test where the summary output is a CSV
	Columns are compared to a static test CSV
	
	name : Name of the test
	input_file : Namelist input file - given as cmd line arg to program
	output_csv : Path to output summary file, assumed csv
	test_csv : Path to test summary file, assumed csv
	col_name : Name of column in both output_csv and test_csv to be compared
	threshold : Mean squared error threshold for testing
	
	"""
	name : str
	input_file : str
	output_csv : str
	test_csv : str
	col_name : str
	threshold : float

def get_input(test):
	"""
	
	Assumed Fortran program input is in a namelist 
	Passed as cmd line arg
	
	"""

	input_file = test.input_file
	nml = f90nml.read(input_file)

	# Get number of processors needed for run
	# Assume this is stored in MPI/nproc
	# Modify as appropriate
	nproc = nml['MPI']['nproc']

	return input_file,nproc

def run_mpiexec_program(test):
	"""
	
	Runs the test given, this uses subprocess to call the mpi program

	Catches errors and screen outputs of the program
	
	"""
	input_file,nproc = get_input(test)

	# Create command and execute
	exe_cmd = f"{mpiexec} -n {nproc} {exe_file} {input_file}"
	fortran_program = subprocess.Popen(exe_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell=True)
	
	# Get screen outputs and error messages and save to files
	out,err = fortran_program.communicate()
	if out!=None and out!="":
		out=str(out,'utf-8')
		with open(output_dir+f"program_output_{test.name}.txt",'w') as f:
			f.write(out)
	if err!=None and err!="":
		err=str(err,'utf-8')
		with open(output_dir+f"program_error_{test.name}.txt",'w') as f:
			f.write(err)
	fortran_program.wait()

	# Print error message to screen after code completion
	if err != "":
		print("Program Error Message:")
		with open(output_dir+f"program_error_{test.name}.txt", 'r') as fin:
			print(fin.read())
