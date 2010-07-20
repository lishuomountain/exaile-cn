# This Python file uses the following encoding: utf-8
#       
#       Copyright 2009 Bill Ma <billnowar@gmail.com>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.

from xlgui.preferences import widgets
import os
from xl.nls import gettext as _
from xl import event

name = _('LyricDisp')
basedir = os.path.dirname(os.path.realpath(__file__))
ui = os.path.join(basedir, "prefs.ui")

class LyricFolderPreference(widgets.Preference):
    default = '~/lyrics'
    name = 'plugin/LyricDisp/lf'
    
class LyricSpacing(widgets.Preference):
    default = '2'
    name = 'plugin/LyricDisp/lyricspacing'

class LyricColor(widgets.ColorButtonPreference):
    def _setup_change(self):
        widgets.ColorButtonPreference._setup_change(self)
    def change(self, *args):
        event.log_event('color_change', self, self._get_value())
    default = '#43AAD0'
    name = 'plugin/LyricDisp/lc'

class ModePreference(widgets.ComboPreference):
    default = '窗口模式'
    name = 'plugin/LyricDisp/ms'
    def _setup_change(self):
        widgets.ComboPreference._setup_change(self)
    def change(self, *args):
        event.log_event('mode_change', self, self._get_value())

class LyricNamePreference(widgets.ComboPreference):
    default = 'artist-title.lrc'
    name = 'plugin/LyricDisp/ln'
    def _setup_change(self):
        widgets.ComboPreference._setup_change(self)
    def change(self, *args):
        event.log_event('name_change', self, self._get_value())
