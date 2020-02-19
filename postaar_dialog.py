# -*- coding: utf-8 -*-
"""
/***************************************************************************
 postAARDialog
                                 A QGIS plugin
 This plugin detects points forming a rectangular within defined margins to mark potential houses  
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2019-06-13
        git sha              : $Format:%H$
        copyright            : (C) 2019 by ISAAKiel
        email                : isaak@ufg.uni-kiel.de
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os

from PyQt5 import QtCore, uic, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QApplication, QFileDialog
from qgis.gui import QgsMessageBar
from qgis.utils import iface

# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'postaar_dialog_base.ui'))


class postAARDialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(postAARDialog, self).__init__(parent)
        self.setupUi(self)
        self.setSizeGripEnabled(False);
        self.setWindowFlags(QtCore.Qt.Dialog | QtCore.Qt.MSWindowsFixedSizeDialogHint)
        
        self.pBSelectPythonDistribution.clicked.connect(self.selectPythonDistribution)

        if not self.lEPythonDistribution.text():
            import platform
            executable = ""
            if platform.system() == 'Windows':
                executable = os.path.join(os.__file__.split("lib")[0],"python")
            if platform.system() == 'Linux' or platform.system() == 'Darwin':
                executable = sys.executable

            self.lEPythonDistribution.setText(str(executable))

    def selectPythonDistribution(self):
        self.lEPythonDistribution.setText(str(QFileDialog.getOpenFileName(self, 'Select distribution')[0]))

    def accept ( self ):
        validInput = self.checkvalues()
        if validInput:
            self.done ( 1 )
        
        # self.accepted.connect(self.checkvalues)
        # if self.checkvalues == 0:
        #     print('checkvalues: ' + str(checkvalues))
        #     self = 0

    def checkvalues(self):
        # Input values have to be checked
        postlayer = self.cmb_layer_selected.currentLayer()
        postid = self.cmb_postid.currentField()
        maximum_length_of_side = self.maximum_length_of_side.value()
        minimum_length_of_side = self.minimum_length_of_side.value()
        max_diff_side = self.maximal_length_difference.value()

        msg = "Please update the data\n\n"

        maximum_length_of_diagonal = self.maximum_length_of_diagonal.value()
        minimum_length_of_diagonal = self.minimum_length_of_diagonal.value()
        
        if maximum_length_of_diagonal < minimum_length_of_diagonal:
                msg = msg + "-  Maximal length of diagonal must be greater or equal to minimal length.\n"

        # Layer selected?
        if not postlayer:
            msg = msg + "-  Please select (active) a Layer.\n" 
        else:
            if postlayer.crs().isGeographic() == True:
                msg = msg + "-  Layer " + postlayer.name() + " is not projected. Please choose an projected reference system. \n"
            # geometry type is point?
            if postlayer.geometryType() != 0:
                msg = msg + "-  Layer " + postlayer.name() + " is not a point geometry. Please choose an point geometry.\n"

        # ID field selected?
        if not postid:
            msg = msg + "-  Please select an ID field.\n" 

        # max length >= min length
        if maximum_length_of_side < minimum_length_of_side:
            msg = msg + "-  Maximal length of side must be greater or equal to minimal length.\n"

        if len(msg) > 30:
            QMessageBox.critical(self, "postAAR input error", msg)
            return False

        # the id column has unique values?
        iface.messageBar().pushMessage("Info", "Checking for duplicate ID's")
        postslist=[]
        for f in postlayer.getFeatures():
            pid = f[postid]
            postslist.append(pid)

        seen = []
        duplicates = []
        for x in postslist:
            if x in seen:
                duplicates.append(x)
            seen.append(x)

        if len(duplicates) > 0:
            msg = "Selected field "+ postid + " has duplicate values:" + str(len(duplicates))
            msg = msg + "\nFirst duplicate value: " + str(duplicates[0])
            msg = msg + "\n\n Press [OK] to continue [Cancel] to exit."
            resp = QMessageBox.question(self, 'postAAR input dialog', msg, QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Ok)
            if resp != 1024:
                return False
        return True