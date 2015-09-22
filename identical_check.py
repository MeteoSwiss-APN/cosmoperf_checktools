#!/usr/bin/env python2

"""
COSMO TECHNICAL TESTSUITE

This script checks whether two runs are bit-identical by comparing the
YUPRTEST files.
"""

# built-in modules
import os, re, sys

# private modules
sys.path.append("./tools") # this is the generic folder for subroutines
sys.path.append('../checktools/tools') 
from ts_utilities import read_environ, dir_path
from ts_fortran_nl import get_param
import comp_yuprtest

# information
__author__     = "Nicolo Lardelli, Oliver Fuhrer"
__copyright__  = "Copyright 2012, COSMO Consortium"
__license__    = "GPL"
__version__    = "1.0"
__date__       = "Mon Oct  8 15:37:57 CEST 2012"
__email__      = "cosmo-wg6@cosmo.org"
__maintainer__ = "xavier.lapillonne@meteoswiss.ch"

# some global definitions
yufile = 'YUPRTEST'   # name of special testsuite output
yuswitch = 'lyuprdbg' # namelist switch controlling YUPRTEST output
nlfile = 'INPUT_ORG'  # namelist file containing lyuprtest and dt


def check():

    # get name of myself
    myname = os.path.basename(__file__)
    header = myname+': '

    # get environment variables
    env = read_environ()
    verbose = int(env['VERBOSE'])
    rundir = dir_path(env['RUNDIR'])
    refoutdir = dir_path(env['REFOUTDIR'])
   
    # defines the 2 file that belongs logically to the checker
    yufile1 = rundir + yufile
    yufile2 = refoutdir + yufile

    # extract timestep
    try:
        dt = float(get_param(rundir+nlfile, 'dt'))
    except:
        if verbose:
            print header+'failed to extract dt from '+rundir+nlfile
        return 20 # FAIL
    
    # check if special testsuite output was actived
    if get_param(rundir+nlfile, yuswitch) in ['.FALSE.', '.false.']:
        if verbose:
            print yuswitch+' is set to .false. in '+rundir+nlfile+' for this simulation'
            return 20 # FAIL

    # define tolerances for comparing YUPRTEST files
    nts = [10000]
    tols = [0.0]
    tas = [0.0]

    try:
        # check for bit identical results
        if verbose>1:
            print header + 'Checking if results are bit identical'
        if verbose>2:
            print header + 'comp_yuprtest()'
            print header + '  file1 = '+yufile1
            print header + '  file2 = '+yufile2
            print header + '  minval = '+str(-1)
            print header + '  nts = [%s]' % ','.join(map(str, nts))
            print header + '  tols = [%s]' % ','.join(map(str, tols))
            print header + '  tas = [%s]' % ','.join(map(str, tas))
        error_count = comp_yuprtest.cmp_(yufile1, yufile2, 0, -1, nts, tols, tas)
        if verbose>1:
            if error_count==0:
                print header + 'Results are bit identical'
            else:
                print header + 'Results are not bit identical'

    except RuntimeError as e:
        if verbose:
            print e
        return 20 # FAIL

    if error_count:
        return 20 # FAIL
    else:
        return 0 # MATCH


if __name__ == "__main__":
    sys.exit(check())

