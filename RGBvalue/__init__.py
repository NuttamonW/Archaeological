# -*- coding: utf-8 -*-
"""
/***************************************************************************
 RGBvalue
                                 A QGIS plugin
 This plugin tells RGB value from exact coordinate X and Y which come from user.
                             -------------------
        begin                : 2015-08-02
        copyright            : (C) 2015 by Point
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
    """Load RGBvalue class from file RGBvalue.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .rbg_value import RGBvalue
    return RGBvalue(iface)
