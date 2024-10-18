import os
import sys

if sys.version_info[:2] >= (3, 7):
    os.add_dll_directory(os.path.abspath(os.path.dirname(__file__)) + '/libs')
else:
    os.environ['path'] = os.path.abspath(os.path.dirname(__file__)) + '/libs;' + os.environ['path']

from napari_BVdata.BVMoudle.BVMoudle import BVReader, getHist