# -*- coding: utf-8 -*-
"""
/***************************************************************************
 OriginPoint
                                 A QGIS plugin
 This plugin will tell the origin both X and Y of the image.
                             -------------------
        begin                : 2015-08-03
        copyright            : (C) 2015 by Point and June
        email                : p.pointt@hotmail.com
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
    """Load OriginPoint class from file OriginPoint.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .origin_point import OriginPoint
    return OriginPoint(iface)
