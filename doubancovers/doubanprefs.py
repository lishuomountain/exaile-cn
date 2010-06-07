#! /usr/bin/env python
#
#
# Sun Ning(classicning@gmail.com, http://www.classicning.com)
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 1, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.


import os
from xlgui.prefs import widgets
from xl.nls import gettext as _
from xl import xdg
import logging

logger = logging.getLogger(__name__)

name = _('Douban Covers')
basedir = os.path.dirname(os.path.realpath(__file__))
ui = os.path.join(basedir, 'doubanprefs_pane.ui')


class DoubanAPIKeyPreference(widgets.PrefsItem):
    default = ''
    name = 'plugin/doubancovers/api_key'
    
