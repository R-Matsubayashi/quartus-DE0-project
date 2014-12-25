#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Script for creating new project from the DE0_TOP project
import os
import shutil
import sys

de0_ = "DE0_TOP"
de0 = "DE0 TOP"

def main(argv):
    here = os.path.abspath(os.curdir)

    if (not os.path.basename(here) == 'DE0_TOP') or (len(argv) is not 1):
        sys.stderr.write('Usage: create-new-project.py "project name"\n')
        sys.stderr.flush()
        exit(1)

    name = argv[0]
    desired_name = name.replace(" ", "_")
    # Note: no other validation performed. desired_name must be a valid
    # Verilog-2001 module identifier for correct behavior

    target = os.path.abspath(here + "/../" + desired_name)
    try:
        os.mkdir(target)
        os.mkdir(target + '/V')
    except OSError as err:
        sys.stderr.write(target + " already exists. Exiting.\n")
        exit(1)

    # print target
    print("Working in " + target)
    
    # Files that need only name modification:
    shutil.copyfile(
        here + '/' + de0_ + '.sdc',
        target + '/' + desired_name + '.sdc')
    
    # Files that need no modification:
    shutil.copyfile(
        here + '/' + 'assignment_defaults.qdf',
        target + '/' + 'assignment_defaults.qdf')

    # Files that need modification: .qpf, .qsf, .v

    # Load file strings
    qpf = open(os.path.abspath(here + "/" + de0_ + ".qpf"), 'r').read()
    qsf = open(os.path.abspath(here + "/" + de0_ + ".qsf"), 'r').read()
    v = open(os.path.abspath(here + "/" + de0_ + ".v"), 'r').read()

    # Modify strings
    qpf = qpf.replace(de0_, desired_name).replace(de0, name)
    qsf = qsf.replace(de0_, desired_name).replace(de0, name)
    v = v.replace(de0_, desired_name).replace(de0, name)

    # Open new files and write out contents
    qpfF = open(os.path.abspath(target + "/" + desired_name + ".qpf"), 'w')
    qsfF = open(os.path.abspath(target + "/" + desired_name + ".qsf"), 'w')
    vF = open(os.path.abspath(target + "/" + desired_name + ".v"), 'w')

    qpfF.write(qpf)
    qsfF.write(qsf)
    vF.write(v)

    for file in [qpfF, qsfF, vF]:
        file.close()
    
    print("Done.")

if __name__ == "__main__":
    main(sys.argv[1:])
