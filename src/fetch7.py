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

		#print csvFile
		csvFile = 'http://www.twse.com.tw/ch/trading/exchange/MI_INDEX/MI_INDEX3_print.php?genpage=genpage/Report201408/A11220140826ALL_1.php&type=csv'

		the_page = urllib.urlopen(csvFile).read()
		if len(the_page) == 0:
			print("Got no page\n")
			#continue

		uthe_page = unicode(the_page, 'cp950')
		# TODO: find 1101 to 漲跌符號說明

		#
		# 證券代號, 證券名稱, 成交股數,     成交筆數, 成交金額,      開盤價, 最高價, 最低價, 收盤價, 漲跌(+/-), 漲跌價差, 最後揭示買價, 最後揭示買量, 最後揭示賣價, 最後揭示賣量, 本益比
		# 1101,     台泥,     "11,137,634", "4,308",  "539,339,150", 49.55,  49.55,  48.10,  48.30,  －,        1.25,     48.25,        62,           48.30,        130,          16.15
		# ...
		# 漲跌符號說明:[+ ->漲][- ->跌][X ->不比價]
		urlData = string.split(uthe_page, u'1101')
		if len(urlData) == 1:
			exit()
		urlData = u'1101' + urlData[1]

		b = StringIO(urlData.encode('utf-8'))
		r = csv.reader(b, delimiter=',', quotechar='"')
		for row in r:
		    print row

#
# Test case
#

def main(argv=None):
	t = fetch7()
	t.fetch_TW()

if __name__ == '__main__':
	sys.exit(main())

