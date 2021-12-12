"""Tests execution of all module examples.

Tests should run as fast as possible to enable fast feedback during code
development. This test script aims to only test the execution of examples
e.g. to check for runtime errors if the module's api was changed,
but the example has not yet been updated accordingly.

The directory of each example and the name of the example script to test needs
to be added to the example_list global variable.

No two examples can have the same script name. Note that if a test fails, then
the data structures, e.g. OpenCMISS objects, may not be finalised. Subsequent
tests may fail if they use the same data structures. it is therefore important
to address any test issues in numerical order. To address this issue, proper
cleanup of data structures, e.g. through a callback, is required whenever
an arbitrary error is encountered. This has not yet been implemented in the
module.

Authors: Thiranja Prasad Babarenda Gamage
Organisation: Auckland Bioengineering Institute, University of Auckland
"""

import os
import sys
import unittest
import subprocess
from parameterized import parameterized

example_root_directory = os.path.abspath('../../examples')

# List of examples to test [example directory, example name].
# Note that some of these examples need to be run in order.
example_list = [
    ['tutorial/', '.py', 'tutorial'],
    ['tutorial/', '.ipynb', 'tutorial']
]

# Define the configuration for the examples.
cfg = None

# Postprocessing of example_list to address peculiarities in parameterized
# python module.

# "parameterized" module uses the first array value in the example_list as the
# test name. Reverse order of example directory and example name to allow the
# example name to be used as the test name.
example_list = [example[::-1] for example in example_list[::-1]]

# "parameterized" module runs through tests in reverse order. Reverse order of
# example list such that the examples run in the order as listed in the
# example list above.
example_list = example_list[::-1]

class TestExampleExecution(unittest.TestCase):
    """Class for testing execution of all examples in the example list.

    Note that each example needs to have a main() function. To achieve
    efficient testing, a test=True input argument is passed to the main()
    function. The user can use this to bypass time consuming tasks e.g. for
    mechanics, it can be used to skip the mechanics solves and quickly test the
    infrastructure. Other tests are necessary to verify/validate that the
    mechanics output is correct e.g. comparisons to expected output/analytic
    solutions.
    """
    @parameterized.expand(example_list)
    def test(self, example_name, example_extension, example_dir):
        """Test execution of example scripts.

        The examples are run in their original directories. They have been
        configured to export any output to 'results_test' folder in their
        original directories.

        Args:
            example_name: Name of example to be tested.
            example_dir: Directory name for the example.
        """

        os.chdir(os.path.join(example_root_directory, example_dir))

        if example_extension == '.py':
            # Add example directory (now the current working directory) to
            # python sys path.
            sys.path.insert(0, './')

            # Import example script.
            example = __import__(example_name)

            # Execute example.
            example.main(cfg, test=True)
        else:
            nbexe = subprocess.Popen(
                ['jupyter', 'nbconvert', '{0}'.format(
                    example_name + example_extension),
                 '--execute',
                 '--ExecutePreprocessor.timeout=120'],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)
            output, err = nbexe.communicate()
            check = nbexe.returncode
            if check == 0:
                print('Captured Output: \n {0}\n {1}'.format(output, err))
                # if passed remove the generated html file
                os.remove('{0}.html'.format(example_name))
            else:
                self.assertTrue(False)
                print('Captured Output: \n {0}'.format(err))

        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
