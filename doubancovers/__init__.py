#!/usr/bin/env python
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
#
#

import urllib
import hashlib
import time
import os
from xl.cover import *
from xl import event, common, settings
import logging

import doubanquery
import doubanprefs

logger = logging.getLogger(__name__)
DOUBAN =None

def enable(exaile):
	if(exaile.loading):
		event.add_callback(_enable, 'exaile_loaded')
	else:
		_enable(None, exaile, None)

def disable(exaile):
	providers.unregister('covers', DOUBAN)

def _enable(eventname, exaile, nothing):
	global DOUBAN
	DOUBAN = DoubanCoverSearch()
	providers.register('covers', DOUBAN)
	
def get_prefs_pane():
    return doubanprefs

class DoubanCoverSearch(CoverSearchMethod):
	"""
		Search and retrieve covers from douban
	"""
	name = 'douban'
	type = 'remote'

	def __init__(self):
		self.starttime = 0

	def find_covers(self, track, limit=-1):
		(artist, album) = track.get_tag_raw('artist')[0], \
			track.get_tag_raw('album')[0]
		return self.search_covers("%s, %s" %(artist, album), limit)

	def search_covers(self, search, limit=-1):
		waittime = 1 - (time.time() - self.starttime)
		if waittime > 0: time.sleep(waittime)
		self.starttime = time.time()

		apikey = settings.get_option('plugin/doubancovers/api_key', None)

		try:
			cover_urls = list(doubanquery.search(search, apikey))
			if len(cover_urls) == 0:
				return []
		except:
			return []

		candidants = []
		for cover_url in cover_urls:
			try:
				candidants.append(cover_url)
			except:
				return []

		return candidants

	def get_cover_data(self, url):
		h = urllib.urlopen(url)
		data = h.read()
		h.close()
		return data

