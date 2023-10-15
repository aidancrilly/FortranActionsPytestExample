# FortranActionsPytestExample
An example set of scripts for building and testing parallel (MPI) Fortran code to allow continuous integration. 

The contained files are:

- workflows/build_and_test.yml - Workflow file
- workflows/python_testing_requirements.txt - Contains required python packages for testing which will be pip installed
- testing/executable_interface.py - Python interface to mpi and compiled fortran code
- testing/test_example.py - Example test script utilising the executable interface

This repo gives a somewhat generic testing workflow framework for parallel (MPI) Fortran programs based on my experience with implementing similar. It can be adapted to your use case assumes the following program structure:

- Fortran program compiled using makefile and mpiifort from Intel oneAPI
- Fortran program takes namelist input file which specifies number of processors needed
- Output to be tested is in form of a csv which is compared to a test example

The workflow file is configured for a RedHat Enterprise runner.

If one is using separate code and testing data repositories, then workflow includes the steps required to clone the testing data repo. The neatest solution in terms of SSH keys seems to be the following:

- The data repository requires a deploy key such that it can be cloned during workflow testing.
- The corresponding private key needs to be a secret of the code repository.

See top answer of this Stack Overflow: [link](https://stackoverflow.com/questions/60222741/github-actions-and-git-clone-issue)

