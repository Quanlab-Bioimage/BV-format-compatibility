"""napari-cellseg3d: napari plugin for 3D cell segmentation.

Main plugins menu for napari-cellseg3d.
"""

from napari_BVdata.code_plugins.cl_plugin_review import Reviewer

def napari_experimental_provide_dock_widget():
    return [
        (Reviewer, {"name": "Review loader"})
    ]
