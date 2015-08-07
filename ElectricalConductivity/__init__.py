# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ElectricalConductivity
                                 A QGIS plugin
 This plugin calculates the electrical conductivity in soil for each pixel in the image which red channel represents variations in soil sand content,  green channel represents variations in soil clay content, and  blue channel represents variations in soil organic matter (OM) content.
                             -------------------
        begin                : 2015-08-04
        copyright            : (C) 2015 by Point & June
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
    """Load ElectricalConductivity class from file ElectricalConductivity.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .electrical_conductivity import ElectricalConductivity
    return ElectricalConductivity(iface)
