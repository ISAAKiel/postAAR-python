# -*- coding: utf-8 -*-
"""
/***************************************************************************
 postAAR
                                 A QGIS plugin
 This plugin detects points forming a rectangular within defined margins to mark potential houses  
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2019-06-13
        copyright            : (C) 2019 by ISAAKiel
        email                : isaak@ufg.uni-kiel.de
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load postAAR class from file postAAR.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .postaar import postAAR
    return postAAR(iface)
