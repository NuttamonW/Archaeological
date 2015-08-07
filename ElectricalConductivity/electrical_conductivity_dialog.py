# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ElectricalConductivityDialog
                                 A QGIS plugin
 This plugin calculates the electrical conductivity in soil for each pixel in the image which red channel represents variations in soil sand content,  green channel represents variations in soil clay content, and  blue channel represents variations in soil organic matter (OM) content.
                             -------------------
        begin                : 2015-08-04
        git sha              : $Format:%H$
        copyright            : (C) 2015 by Point & June
        email                : p.pointt@hotmail.com
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

from PyQt4 import QtGui, uic

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'electrical_conductivity_dialog_base.ui'))


class ElectricalConductivityDialog(QtGui.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(ElectricalConductivityDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
