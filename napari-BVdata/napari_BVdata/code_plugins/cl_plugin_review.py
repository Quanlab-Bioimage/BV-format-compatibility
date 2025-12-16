"""Review plugin for 3D labeling of volumes."""
from pathlib import Path

import matplotlib.pyplot as plt
import napari
import numpy as np
from magicgui import magicgui
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
)
from matplotlib.figure import Figure

# Qt
from qtpy.QtWidgets import QTabWidget, QWidget
from qtpy.QtWidgets import QLineEdit, QSizePolicy
from tifffile import imwrite

# local
from napari_BVdata import utils
from napari_BVdata import interface as ui
from napari_BVdata.code_plugins.plugin_base import BasePluginSingleImage

# logger = utils.LOGGER

from qtpy.QtWidgets import QPushButton, QInputDialog, QVBoxLayout, QLineEdit, QDialog, QLabel, QHBoxLayout, QFileDialog, QSpinBox, QGroupBox
from napari_BVdata.BVMoudle import BVReader

class Reviewer(QTabWidget):
    """A plugin for selecting volumes and labels file and launching the review process.

    Inherits from : :doc:`plugin_base`.
    """

    def __init__(self, viewer: "napari.viewer.Viewer", parent=None):
        """Creates a Reviewer plugin with several buttons.

        * Open file prompt to select volumes directory

        * Open file prompt to select labels directory

        * A dropdown menu with a choice of png or tif filetypes

        * A checkbox if you want to create a new status csv for the dataset

        * A button to launch the review process
        """
        super(Reviewer, self).__init__(parent)
        self._viewer = viewer
        self._build()
        self.reader = BVReader()

    def _build(self):
        """Build buttons in a layout and add them to the napari Viewer."""
        cl_tab = ui.ContainerWidget(0, 0, 1, 1)
        self.addTab(cl_tab, "LOAD")
        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.MinimumExpanding)
        cl_layout = cl_tab.layout

        group_box = QGroupBox(title="Data info")
        config_layout = QVBoxLayout()
        group_box.setLayout(config_layout)
        head_label1 = QLabel("File info")
        config_label = QLabel("Select config file:")
        config_button = QPushButton('Browse')

        config_file_path = QLineEdit()
        config_file_path.setReadOnly(True)

        data_size_label = QLabel("Data size: ")
        data_size_layout = QHBoxLayout()
        data_size_layout.addWidget(data_size_label)
        data_size = QLineEdit()
        data_size.setReadOnly(True)
        data_size_layout.addWidget(data_size)

        def select_config_file():
            file_dialog = QFileDialog()
            file_dialog.setNameFilter("Config Files (*.cfg)")
            if file_dialog.exec_():
                config_file = file_dialog.selectedFiles()[0]
                config_file_path.setText(config_file)
                # scale = loadConfig(config_file).contents.bigImgSizek
                scale = self.reader.readConfig(config_file)['bigImgSize']
                data_size.setText(str(scale[0]) + " * " + str(scale[1]) + " * " + str(scale[2]))
                spin_boxx1.setRange(0, scale[0])
                spin_boxx1.setValue(0)
                spin_boxx2.setRange(0, scale[0])
                spin_boxx2.setValue(scale[0])

                spin_boxy1.setRange(0, scale[1])
                spin_boxy1.setValue(0)
                spin_boxy2.setRange(0, scale[1])
                spin_boxy2.setValue(scale[1])

                spin_boxz1.setRange(0, scale[2])
                spin_boxz1.setValue(0)
                spin_boxz2.setRange(0, scale[2])
                spin_boxz2.setValue(scale[2])

        config_button.clicked.connect(select_config_file)
        config_layout.addWidget(config_label)
        config_layout.addWidget(config_button)
        config_layout.addWidget(config_file_path)
        config_layout.addLayout(data_size_layout)

        group_box2 = QGroupBox(title="Setting ROI")
        config_layout2_ = QVBoxLayout()
        config_layout2 = QHBoxLayout()
        group_box2.setLayout(config_layout2_)

        L1 = QVBoxLayout()
        name_label0 = QLabel("")
        x_label = QLabel("X")
        x_label.setFixedWidth(30)
        y_label = QLabel("Y")
        y_label.setFixedWidth(30)
        z_label = QLabel("Z")
        z_label.setFixedWidth(30)
        L1.addWidget(name_label0)
        L1.addWidget(x_label)
        L1.addWidget(y_label)
        L1.addWidget(z_label)
        config_layout2.addLayout(L1)

        L2 = QVBoxLayout()

        name_label1 = QLabel("Begin")
        spin_boxx1 = QSpinBox()
        spin_boxy1 = QSpinBox()
        spin_boxz1 = QSpinBox()
        L2.addWidget(name_label1)
        L2.addWidget(spin_boxx1)
        L2.addWidget(spin_boxy1)
        L2.addWidget(spin_boxz1)
        config_layout2.addLayout(L2)

        L3 = QVBoxLayout()
        # L3.setSpacing(0)
        # L3.setContentsMargins(0, 0, 0, 0)

        name_label2 = QLabel("End")
        spin_boxx2 = QSpinBox()
        spin_boxy2 = QSpinBox()
        spin_boxz2 = QSpinBox()
        L3.addWidget(name_label2)
        L3.addWidget(spin_boxx2)
        L3.addWidget(spin_boxy2)
        L3.addWidget(spin_boxz2)
        config_layout2.addLayout(L3)

        level_layout = QHBoxLayout()
        level_label = QLabel("level ")
        level_box = QSpinBox()
        level_box.setRange(0, 4)
        level_box.setValue(2)
        level_layout.addWidget(level_label)
        level_layout.addWidget(level_box)

        config_layout2_.addLayout(config_layout2)
        config_layout2_.addLayout(level_layout)

        def on_x1_value_changed(value):
            spin_boxx2.setMinimum(value)

        def on_x2_value_changed(value):
            spin_boxx1.setMaximum(value)

        def on_y1_value_changed(value):
            spin_boxy2.setMinimum(value)

        def on_y2_value_changed(value):
            spin_boxy1.setMaximum(value)

        def on_z1_value_changed(value):
            spin_boxz2.setMinimum(value)

        def on_z2_value_changed(value):
            spin_boxz1.setMaximum(value)

        spin_boxx1.valueChanged.connect(on_x1_value_changed)
        spin_boxx2.valueChanged.connect(on_x2_value_changed)
        spin_boxy1.valueChanged.connect(on_y1_value_changed)
        spin_boxy2.valueChanged.connect(on_y2_value_changed)
        spin_boxz1.valueChanged.connect(on_z1_value_changed)
        spin_boxz2.valueChanged.connect(on_z2_value_changed)

        def BV_load(_minx, _maxx, _miny, _maxy, _minz, _maxz, _level, _path):
            param = [_path,  # 配置文件路径
                     _level,  # 级别
                     _minx,  # xmin 883
                     _maxx,  # xmax 9162
                     _miny,  # ymin 2260
                     _maxy,  # ymax 9565
                     _minz,  # zmin 344
                     _maxz]  # zmax 1318
            dataPtr = self.reader.loadROI(_path, _level, _minx, _maxx, _miny, _maxy, _minz, _maxz)
            return dataPtr

        def on_ok():
            img = BV_load(spin_boxx1.value(), spin_boxx2.value(), spin_boxy1.value(), spin_boxy2.value(),
                          spin_boxz1.value(), spin_boxz2.value(), level_box.value()
                          , config_file_path.text())
            image_layer = self._viewer.add_image(img, rendering='mip', name='volume', blending='additive', opacity=1.0)
            image_layer.bounding_box.visible = True
            image_layer2 = self._viewer.add_image(img, rendering='mip', name='volume', blending='additive', opacity=1.0,
                                            colormap='green')
            image_layer2.bounding_box.visible = True

        ok_button = QPushButton("OK")
        ok_button.clicked.connect(on_ok)
        config_layout2_.addWidget(ok_button)

        cl_layout.addWidget(group_box)
        ui.add_blank(self, cl_layout)
        cl_layout.addWidget(group_box2)

        tab = ui.ContainerWidget(0, 0, 1, 1)
        layout = tab.layout

        ui.ScrollArea.make_scrollable(
            contained_layout=layout, parent=tab, min_wh=[190, 300]
        )

        # self.addTab(tab, "BVdata")
        cl_tab2 = ui.ContainerWidget(0, 0, 1, 1)
        self.addTab(cl_tab2, "LOAD patch")
        cl_layout2 = cl_tab2.layout
        group_box3 = QGroupBox(title="Load data")
        config_layout3 = QVBoxLayout()
        group_box3.setLayout(config_layout3)
        config_label3 = QLabel("Select file:")
        config_button3 = QPushButton('Browse')

        def select_file():
            file_dialog = QFileDialog()
            file_dialog.setNameFilter("Select Files (*.bv)")
            if file_dialog.exec_():
                config_file = file_dialog.selectedFiles()[0]
                file_path.setText(config_file)

        config_button3.clicked.connect(select_file)
        file_path = QLineEdit()
        file_path.setReadOnly(True)
        config_layout3.addWidget(config_label3)
        config_layout3.addWidget(config_button3)
        config_layout3.addWidget(file_path)

        def on_ok2():
            img = self.reader.readBV(file_path.text(), 0, 0)
            image_layer = self._viewer.add_image(img, rendering='mip', name='volume', blending='additive', opacity=1.0)
            image_layer.bounding_box.visible = True
            image_layer2 = self._viewer.add_image(img, rendering='mip', name='volume', blending='additive', opacity=1.0,
                                                  colormap='green')
            image_layer2.bounding_box.visible = True
        ok_button2 = QPushButton("OK")
        ok_button2.clicked.connect(on_ok2)
        config_layout3.addWidget(ok_button2)
        cl_layout2.addWidget(group_box3)

        self.setMinimumSize(180, 100)
