######################################################################
# setup script for the Python wrapper of ODE
######################################################################

from distutils.core import setup, Extension
import distutils.sysconfig
import shutil, os, os.path, sys

# ODE itself must already be compiled

# Windows?
if sys.platform=="win32":
    
    ODE_BASE = "../ode_single_trimesh"
#    ODE_BASE = "../ode_double_notrimesh"
    
    INC_DIRS = [os.path.join(ODE_BASE, "include")]
    LIB_DIRS = [os.path.join(ODE_BASE, "lib")]
    LIBS     = ["ode", "user32"]  # user32 because of the MessageBox() call
    CC_ARGS  = ["/ML"]

# Linux (and other)
else:

    ODE_BASE = "../ode"

    INC_DIRS = [os.path.join(ODE_BASE, "include")]
    LIB_DIRS = [os.path.join(ODE_BASE, "lib")]
    LIBS     = ["ode", "stdc++"]
    CC_ARGS  = []

######################################################################

def determinePrecision():
    filename = os.path.normpath(os.path.join(ODE_BASE, "config", "user-settings"))
    print 'Reading "%s" to determine precision...'%filename
    precision = None
    try:
        for s in file(filename):
            s = s.strip()
            a = s.split("=")
            if len(a)==2 and a[0].upper()=="PRECISION":
                precision = a[1]
    except IOError, e:
        print "ERROR:",e
        raise RuntimeError

    if precision==None:
        print "ERROR: No precision setting found."
        raise RuntimeError
    if precision not in ["SINGLE", "DOUBLE"]:
        print 'ERROR: Invalid precision setting: "%s"'%precision
        raise RuntimeError
    
    return precision

######################################################################

# Determine the precision setting (SINGLE or DOUBLE?)
#try:
#    precisionfile = "_precision.pyx"
#    precision = determinePrecision()
#    print "Precision:",precision
#    print 'Creating file "%s"...'%precisionfile
#    f = file(precisionfile, "wt")
#    f.write("# This file was automatically generated by the setup script\n\n")
#    f.write('cdef extern from "ode/ode.h":\n')
#    f.write('    # Define the basic floating point type used in ODE\n')
#    f.write('    ctypedef %s dReal\n'%{"SINGLE":"float", "DOUBLE":"double"}[precision])
#    f.close()
#except RuntimeError:
#    print "Aborting!"
#    sys.exit()

# Check if the ODE_BASE path does exist
if not os.path.exists(ODE_BASE):
    print """This Python ODE wrapper assumes that you have a compiled version of
the ODE library already somewhere on your system. The path to the ODE
distribution has to be set in the setup script via the variable
ODE_BASE. Currently it points to "%s".
However, that path does not exist. So please change the variable inside the
script so that it points to the actual location of the ODE directory."""%ODE_BASE
    sys.exit()

# Generate the C source file
cmd = "pyrexc -o ode.c -I. -Isrc src/ode.pyx"
print cmd
err = os.system(cmd)
if err!=0:
    print "An error occured while generating the C source file."
    sys.exit(err)


# Compile the module
setup(name="pyODE",
#      version="0.35cvs-2",
      description="Python wrapper for the Open Dynamics Engine",
#      author="Matthias Baas",
#      author_email="baas@ira.uka.de",
#      license="BSD license, see license*.txt",
      packages=["xode"],
      ext_modules=[Extension("ode", ["ode.c"]
                   ,libraries=LIBS
                   ,include_dirs=INC_DIRS
                   ,library_dirs=LIB_DIRS
                   ,extra_compile_args=CC_ARGS)                   
                   ])
