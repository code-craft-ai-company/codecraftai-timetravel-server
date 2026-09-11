This folder is the folder where the 'testroot' folders.

ccai - Is the root directory for 'testbase' tests (the `__testroot__.py` beside it
       declares the root type).  This folder is added to the PYTHONPATH in the debug
       environment in order to make it easy to debug your code.  All tests in this
       repository run under testbase; pytest is not used.
