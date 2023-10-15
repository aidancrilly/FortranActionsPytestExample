from executable_interface import *
import pandas as pd
import numpy as np

# Filling test data class with example variables
ExampleTest = Test_CSVOutput(
    "example",
    "example.nml",
    f"{output_dir}/example/summary.csv",
    f"{data_dir}/example/summary.csv",
    "test_variable",
    1e-5)

def test_example():
    """
    
    Skeleton code for test
    Compare code output to test file via MSE
    
    """

    run_mpiexec_program(ExampleTest)

    # Load output data
    output = pd.read_csv(ExampleTest.output_csv)

    # Load test data
    test = pd.read_csv(ExampleTest.test_csv)

    # Compute mean squared error between relevant columns
    MSE = np.mean((output[ExampleTest.col_name]-test[ExampleTest.col_name])**2)

    assert MSE < ExampleTest.threshold

