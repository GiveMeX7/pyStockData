#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import sys
import string

from datetime import date
import urllib
import urllib2
from StringIO import StringIO
import csv

class fetch7:
	def __init__(self):
		pass

	def fetch_TW(self):
		today = date.today()
		csvFile = 'http://www.twse.com.tw/ch/trading/exchange/MI_INDEX/MI_INDEX3_print.php?genpage=genpage/Report'
		csvFile += str(today.year) + str(today.month).zfill(2) + '/A112'
		csvFile += str(today.year) + str(today.month).zfill(2) + str(today.day).zfill(2) + 'ALL_1.php&type=csv'
		print csvFile

		the_page = urllib.urlopen(csvFile).read()
		if len(the_page) == 0:
			print("Go no page\n")
			#continue

		uthe_page = unicode(the_page, 'cp950')
		# TODO: find 1101 to 漲跌符號說明



#
# Test case
#

def main(argv=None):
	t = fetch7()
	t.fetch_TW()

if __name__ == '__main__':
	sys.exit(main())

