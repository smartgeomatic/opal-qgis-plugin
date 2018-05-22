# -*- coding: utf-8 -*-
"""
/***************************************************************************
 NmapsEngine
                                 A QGIS plugin
 Nmaps engine
                             -------------------
        begin                : 2018-03-11
        copyright            : (C) 2018 by WO
        email                : w.oronski@acrux.net.pl
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
import os
import sys
import site


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load NmapsEngine class from file NmapsEngine.

    :param iface: A QGIS interface instance.
    :type iface: QgisInterface
    """
    #
    site.addsitedir(os.path.abspath(os.path.dirname(__file__) + '/ext-libs'))

    from nmaps_engine import NmapsEngine
    return NmapsEngine(iface)
