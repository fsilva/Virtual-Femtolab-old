# A very simple setup script to create 2 executables.
#
# hello.py is a simple "hello, world" type program, which alse allows
# to explore the environment in which the script runs.
#
# test_wx.py is a simple wxPython program, it will be converted into a
# console-less program.
#
# If you don't have wxPython installed, you should comment out the
#   windows = ["test_wx.py"]
# line below.
#
#
# Run the build process by entering 'setup.py py2exe' or
# 'python setup.py py2exe' in a console prompt.
#
# If everything works well, you should find a subdirectory named 'dist'
# containing some files, among them hello.exe and test_wx.exe.


from distutils.core import setup
import py2exe
import matplotlib

setup(
    # The first three parameters are not required, if at least a
    # 'version' is given, then a versioninfo resource is built from
    # them and added to the executables.
    version = "Preview Release",
    description = "Virtual FemtoLab Preview Release",
    name = "Virtual FemtoLab Preview Release",

    # targets to build
    console = ["main.py"],
        options = {
                  'py2exe': {
                      'packages':'encodings',
                      'includes': 'cairo, pango, pangocairo, atk, gobject',
                  }
              },

    data_files=[
                   'data/RainbowSpectrum.csv',
                   'data/RainbowSpectrum2.csv',
                   'data/APSAW5Lambda4.csv',
                   'data/ThorlabsLambda4.csv',
                   'data/SamplePhase.csv',
               ]+matplotlib.get_py2exe_datafiles()

    )
