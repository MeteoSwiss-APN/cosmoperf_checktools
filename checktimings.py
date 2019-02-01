#!/usr/bin/env python2

"""
COSMO TECHNICAL TESTSUITE

This script checks whether the standard output of the COSMO simulation
contains the words "CLEAN UP" which is indicative of a fully successful
simulation
"""

import sys
# private modules
sys.path.append("./tools") # this is the generic folder for subroutines
sys.path.append('../checktools/tools')
from ts_utilities import read_environ, dir_path
from ts_fortran_nl import get_param

# information
__author__     = "Pascal Spoerri"
__copyright__  = "Copyright 2015, MeteoSwiss"
__license__    = "GPL"
__version__    = "1.0"

def parse():
    from cosmo_timings_yu import COSMO_Run_yu
    env = read_environ()
    rundir = env['RUNDIR']
    yutimings = "YUTIMING"
    cosmolog = env['LOGFILE']
    slurmlog = env['LOGFILE_SLURM']
    name = "Cosmo run in "+rundir
    return COSMO_Run_yu(folder=rundir, name=name, yutimings="YUTIMING", cosmolog=cosmolog, slurmlog=slurmlog)

def get_reference_timings():
    import ConfigParser
    config = ConfigParser.RawConfigParser()
    env = read_environ()
    rundir = env['RUNDIR']
    timings_file = env['TIMINGS']
    file_path = dir_path(rundir)+timings_file
    config.read(file_path)
    threshold = float(config.get('timings', 'threshold'))
    timings = {}
    for name, value in config.items("timings"):
        if name == "threshold":
            continue
        timings[name] = float(value)
    return (timings, threshold)

def check_value(reference, value, threshold=0):
    if value < (reference*(1.0+threshold/100.0)):
        return True
    return False

def check():
    data = parse()
    timings, threshold = get_reference_timings()
    status = 0
    for name, timing_ref in timings.iteritems():
        data_timing = data[name]
        if data_timing is None:
            print("Fail: No timing data available for "+name)
        if not check_value(timing_ref, data_timing, threshold=threshold):
            print("Fail: Could not validate "+name+": timing "+str(data_timing)+" (reference timing: "+str(timing_ref)+" with "+str(threshold)+"% threshold)")
            status = 20
        else:
            print(name+": "+str(data_timing)+"s below reference: "+str(timing_ref)+"s with "+str(threshold)+"% threshold")
    return status
if __name__ == "__main__":
    sys.exit(check())
