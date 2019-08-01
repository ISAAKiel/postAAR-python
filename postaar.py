# -*- coding: utf-8 -*-
"""
/***************************************************************************
 postAAR
                                 A QGIS plugin
 This plugin detects points forming a rectangular to mark potential houses.  
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
from PyQt5.QtCore import QSettings, QTranslator, qVersion, QCoreApplication, QVariant
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QMessageBox 
from qgis.core import *
from qgis.gui import QgsMessageBar
from qgis.utils import iface

# Initialize Qt resources from file resources.py
from .resources import *

# Import the code for the dialog
from .postaar_dialog import postAARDialog
import os.path

# specific functions
from .helper import *
from .algorythm import *
#import .helper as hlp
#import .algorythm as alg



class postAAR:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'postAAR_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&postAAR')

        # Check if plugin was started the first time in current QGIS session
        # Must be set in initGui() to survive plugin reloads
        self.first_start = None

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('postAAR', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            # Adds plugin icon to Plugins toolbar
            self.iface.addToolBarIcon(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/postAAR/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'postAAR - rectangles'),
            callback=self.run,
            parent=self.iface.mainWindow())

        # will be set False in run()
        self.first_start = True

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&postAAR'),
                action)
            self.iface.removeToolBarIcon(action)


    def run(self):
        """Run method that performs all the real work"""
        # initialize the external functions
 
        # Create the dialog with elements (after translation) and keep reference
        # Only create GUI ONCE in callback, so that it will only load when the plugin is started
        if self.first_start == True:
            self.first_start = False
            self.dlg = postAARDialog()
        
        # show the dialog
        self.dlg.show()
        
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            ## Do something useful here - delete the line containing pass and
            ## substitute with your code.
            postlayer = self.dlg.cmb_layer_selected.currentLayer()
            postlayer_crs = postlayer.crs().authid()
            postid = self.dlg.cmb_postid.currentField()
            maximum_length_of_side = int(unicode(self.dlg.maximum_length_of_side.text()))
            minimum_length_of_side = int(unicode(self.dlg.minimum_length_of_side.text()))
            max_diff_side = float(unicode(self.dlg.maximal_length_difference.text()))
            results_shape = unicode(self.dlg.save_outfile.filePath())

            # write feature id, x, y into a general base list to secure order of the features
            postslist=[]
            for f in postlayer.getFeatures():
                pid = f[postid]
                x = f.geometry().asPoint().x()
                y = f.geometry().asPoint().y()
                postslist.append([pid, x, y])
            x_values = []
            y_values = []
            for p in postslist:
                x_values.append(p[1])
                y_values.append(p[2])

            windows = buildWindows(x_values, y_values, min(x_values) - 1, max(x_values) + 1, min(y_values) - 1, max(y_values) + 1, maximum_length_of_side)

            found_rects = find_rects(windows, x_values, y_values, maximum_length_of_side, minimum_length_of_side, max_diff_side) #,  number_of_computercores=number_of_computercores)
                
            buildings = findBuildings(found_rects, x_values, y_values)
            buildings.sort(key=lambda l : len(l), reverse=True)

            msg = "rectangles found: " + str(len(found_rects)) + "\n" + "buildings found: " + str(len(buildings))
            
            QMessageBox.information(None, "postAAR", msg)
            #print (str(found_rects[0]))
            #print (str(buildings[0]))

            # Creat results layer in memory
            results_layer = iface.addVectorLayer("Polygon?crs="+postlayer_crs, "found_rectangles", "memory")
            # if the loading of the layer fails, give a message
            if not results_layer:
                criticalMessageToBar(self, 'Error', 'Failed to load the file '+ results_shape)
            # add basic attributes
            pr = results_layer.dataProvider()
            pr.addAttributes([QgsField("ID", QVariant.String), 
                                QgsField("PostIDs", QVariant.String), 
                                QgsField("max_diff_sides", QVariant.Double)])
            results_layer.updateFields()
            # add the rectangles by a point list build first
            i=0
            for r in found_rects:
                #print(r)
                i=i+1
                listPoints = []
                PIDs = ""
                plist = r[0]
                #print (plist)
                for p in plist[:4]:
                    listPoints.append(QgsPointXY(x_values[p], y_values[p]))
                    print(listPoints)
                    PIDs = PIDs + str(postslist[p][0]) + "-"
                max_diff_side_rectangle = r[1]

                fet = QgsFeature()
                fet.setGeometry(QgsGeometry.fromPolygonXY ([listPoints]))
                fet.setAttributes([1, PIDs, max_diff_side_rectangle])
                pr = results_layer.dataProvider()
                pr.addFatures([fet])
                results_layer.updateExtends()

