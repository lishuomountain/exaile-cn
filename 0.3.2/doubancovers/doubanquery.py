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
import json
import sys
import logging
reload(sys)
sys.setdefaultencoding("utf-8")
logger = logging.getLogger(__name__)

def search(key, apikey=None):
	quoted = urllib.quote(key.encode("utf8"))
	urltemplate="http://api.douban.com/music/subjects?q=%s&max-results=5&alt=json"
	query = urltemplate %(quoted)
	
	if apikey:
		urltemplate += ("&api_key=%s" % apikey)
	
	h = urllib.urlopen(query)
	data = h.read()


	result = json.loads(data)
	if(len(result['entry'])>0):
		for entry in result['entry']:
			links = entry['link']
			for link in links:
				if link['@rel'] == 'image':
					yield link['@href']

if __name__ == '__main__':
	print list(search('The Innocence Mission, Now the day is over'));
	

