# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ElectricalConductivity
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
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt4.QtGui import QAction, QIcon, QFileDialog
# Initialize Qt resources from file resources.py
import resources_rc
# Import the code for the dialog
from electrical_conductivity_dialog import ElectricalConductivityDialog
import os.path
import gdal
import math
import Image
from qgis.core import QgsRasterLayer, QgsPoint, QgsRaster


class ElectricalConductivity:
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
            'ElectricalConductivity_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = ElectricalConductivityDialog()

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Electrical Conductivity')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'ElectricalConductivity')
        self.toolbar.setObjectName(u'ElectricalConductivity')
        
        self.dlg.Path.clear()
        self.dlg.browse.clicked.connect(self.select_input_file)
		
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
        return QCoreApplication.translate('ElectricalConductivity', message)


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
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToRasterMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/ElectricalConductivity/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'electrical conductivity'),
            callback=self.run,
            parent=self.iface.mainWindow())


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginRasterMenu(
                self.tr(u'&Electrical Conductivity'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar

    def select_input_file(self):
        filename = QFileDialog.getOpenFileName(self.dlg, "Select input file ","", '*.tif')
        self.dlg.Path.setText(filename)
		
    def run(self):
        """Run method that performs all the real work"""
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            """read path from user input"""
            inputPath = self.dlg.Path.text()
            """set path for output file and concat file name to path"""
            outputPath = 'C:\Users\Administrator\Desktop\\'
            outputName = self.dlg.fileName.text()
            outputFile = outputPath + outputName
             
            """read image and calculate electrical conductivity and electrical Resistivity and set RGB for each pixel which R represent adj Pred Moist,
            G represents electrical conductivity and B represents electrical resistivity"""
            """for tiff file output"""
            if(self.dlg.tiff.isChecked()):
                oldImage = Image.open(inputPath)
                rgb_image = oldImage.convert('RGB')
                newImage = Image.new(oldImage.mode,oldImage.size,'white')
                for x in xrange(newImage.size[0]):
                    for y in xrange(newImage.size[1]):
                        R, G, B = rgb_image.getpixel((x, y))
                        sand = (R * 0.4 / 255.0)
                        clay = (G * 0.5 / 255.0)
                        om = (B * 5 / 255.0)
                        predMoist = -0.251 * sand + 0.195 * clay + 0.011 * om + 0.006 * sand * om - 0.027 * clay * om + 0.452 * sand * clay + 0.299
                        adjPredMoist = predMoist + (1.283 * predMoist * predMoist - 0.374 * predMoist - 0.015)
                        electricalConductivity = 0.000471052 * math.pow(100 * adjPredMoist, 3.458)
                        electricalResistivity = 1000.0 / electricalConductivity
                        newImage.putpixel((x,y),(int(adjPredMoist), int(electricalConductivity), int(electricalResistivity)))
                newImage.save(outputFile + '.tif')
            
            """create raster layer and calculate electrical conductivity and write in ASCII XYZ file which X and Y represent centroid coordinate of each pixel
            and Z represents electrical conductivity"""
            """for ASCII XYZ file output"""
            if(self.dlg.asciiXYZ.isChecked()):
                raster = QgsRasterLayer(inputPath)
                w = raster.width()
                h = raster.height()
                p = raster.dataProvider()
                b = p.block(0, p.extent(), w, h)
                f = file(outputFile + '.xyz', 'w')
                f.write('X,Y,Z(Electrical Conductivity)\n')
                pix_x = raster.rasterUnitsPerPixelX()
                pix_y = raster.rasterUnitsPerPixelY()
                half_x = pix_x / 2
                half_y = pix_y / 2
			
                extent = p.extent()
			
                count = 0
                y = extent.yMinimum()
                while y < extent.yMaximum():
                    y += pix_y
                    count += 1
                    x = extent.xMinimum()
                    while x < extent.xMaximum():
                        x += pix_x
                        pos = QgsPoint(x - half_x, y - half_y)
                        R = p.identify(pos, QgsRaster.IdentifyFormatValue).results()[1]
                        G = p.identify(pos, QgsRaster.IdentifyFormatValue).results()[2]
                        B = p.identify(pos, QgsRaster.IdentifyFormatValue).results()[3]
                        sand = (R * 0.4 / 255.0)
                        clay = (G * 0.5 / 255.0)
                        om = (B * 5 / 255.0)
                        predMoist = -0.251 * sand + 0.195 * clay + 0.011 * om + 0.006 * sand * om - 0.027 * clay * om + 0.452 * sand * clay + 0.299
                        adjPredMoist = predMoist + (1.283 * predMoist * predMoist - 0.374 * predMoist - 0.015)
                        electricalConductivity = 0.000471052 * math.pow(100 * adjPredMoist, 3.458)
                        f.write('%s, %s, %s\n' % (pos.x(),pos.y(), electricalConductivity))
                f.close()
				
				
                 
