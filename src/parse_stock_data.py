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
import os

from datetime import date
import urllib
import urllib2
from StringIO import StringIO
import csv
import sqlite3

class STOCK_ITEM:
    TOTAL_ITEMS     = 23
    number          = 0
    name            = 1
    turnover_shares = 2
    traded_items    = 3
    turnover        = 4
    open_price      = 5
    max_price       = 6
    min_price       = 7
    close_price     = 8
    date            = 16
    MA5             = 17
    MA10            = 18
    MA20            = 19
    MA60            = 20
    MA120           = 21
    MA240           = 22

class fetch7:
    def __init__(self):
        pass

    def fetch_TW_by_date(self, year, month, day):
        today = date.today()
        csvFile = 'http://www.twse.com.tw/ch/trading/exchange/MI_INDEX/MI_INDEX3_print.php?genpage=genpage/Report'
        csvFile += str(year) + str(month).zfill(2) + '/A112'
        csvFile += str(year) + str(month).zfill(2) + str(day).zfill(2) + 'ALL_1.php&type=csv'
        print csvFile

        the_page = urllib.urlopen(csvFile).read()
        if len(the_page) == 0:
            print("Go no page\n")
            return

        csvFile_name = 'A112' + str(year) + str(month).zfill(2) + str(day).zfill(2) + 'ALL_1.csv'
        csvFile = open(csvFile_name, 'wb')
        csvFile.write(the_page)
        csvFile.close()

    def open_create_db(self, databasename):
        global conn
        global db
        conn = sqlite3.connect(databasename)
        conn.text_factory = str
        db = conn.cursor()
        conn.commit()

    def close_db(self):
        global conn
        conn.close()

    def create_table_by_stockID(self, stockID):
        global conn
        global db
        global table

        checkTableExistedCmd = ""
        table = 'RawData' + str(stockID)
        checkTableExistedCmd = "SELECT name FROM sqlite_master WHERE type='table' AND name="
        checkTableExistedCmd+= '\'' + table + '\''
        #print checkTableExistedCmd
        db.execute(checkTableExistedCmd)
        get_table_data=db.fetchall()
        if (len(get_table_data)>0):
            #print checkTableExistedCmd
            checkTableExistedCmd = ""
        else:
            command = 'create table if not exists ' + table
            #command += ' (number, name, turnover_shares, traded_items, turnover, open_price, max_price, min_price, close_price, up_or_down, price_diff, last_buy_price, last_buy_volume, last_sell_price, last_sell_volume, PER, date)'
            command += ' (number, name, turnover_shares, traded_items, turnover, open_price, max_price, min_price, close_price, up_or_down, price_diff, \
                          last_buy_price, last_buy_volume, last_sell_price, last_sell_volume, PER, date, \
                          MA5, MA10, MA20, MA60, MA120, MA240)'
            if (db.execute(command) != -1):
                conn.commit()

    def create_table(self, year, month, day):
        global conn
        global db
        global table
        table = 'RawData' + str(year) + str(month).zfill(2) + str(day).zfill(2)
        command = 'create table if not exists ' + table
        command += ' (number, name, turnover_shares, traded_items, turnover, open_price, max_price, min_price, close_price, up_or_down, price_diff, \
                      last_buy_price, last_buy_volume, last_sell_price, last_sell_volume, PER, \
                      MA5, MA10, MA20, MA60, MA120, MA240)'
        db.execute(command)
        conn.commit()

    def fetch_stock_info_by_date(self, year, month, day):
        global csvFileName
        csvFile = 'http://www.twse.com.tw/ch/trading/exchange/MI_INDEX/MI_INDEX3_print.php?genpage=genpage/Report'
        csvFile += str(year) + str(month).zfill(2) + '/A112'
        csvFile += str(year) + str(month).zfill(2) + str(day).zfill(2) + 'ALL_1.php&type=csv'
        csvFileName = 'A112' + str(year) + str(month).zfill(2) + str(day).zfill(2) + 'ALL_1.csv'
        the_page = urllib.urlopen(csvFile).read()
        if len(the_page) == 0:
            print("Go no page\n")
            return
        csvFile_name = 'A112' + str(year) + str(month).zfill(2) + str(day).zfill(2) + 'ALL_1.csv'
        csvFile = open(csvFile_name, 'wb')
        csvFile.write(the_page)
        csvFile.close()

    def import_data_to_database_by_StockID(self, year, month, day):
        #table_item_count = "23"
        IsValidEntry = True
        localSavedFileName = 'A112' + str(year) + str(month).zfill(2) + str(day).zfill(2) + 'ALL_1.csv'
        fp_today_data = open(localSavedFileName, "r")
        ary_single_line = []
        ary_refined_string = [None] * int(STOCK_ITEM.TOTAL_ITEMS)
        
        while True:            
            line_data = fp_today_data.readline()
            if not line_data: break
            ary_single_line = line_data.split(',')
            #ary_refined_string = line_data.split(',')
            str_len = len(ary_single_line[0])            

            if (str_len != 4):
                continue
             
            if (ary_single_line[0].isdigit() == False):
                continue
            currentStockID = ary_single_line[0]
            
            ary_size = len(ary_single_line)
            #print ary_size
            

            start_to_cat_string = False
            final_str = ""
            item_count = 0;
            for index in range(ary_size):                
                temp_string = ary_single_line[index]
                temp_string = temp_string.replace(',', '')
                if '\"' in temp_string:
                    if (start_to_cat_string==True):
                        start_to_cat_string = False
                    else:
                        start_to_cat_string = True

                temp_string = temp_string.replace('\"', '')

                if (start_to_cat_string==True):
                    final_str += temp_string
                else:
                    if (len(final_str) == 0):
                        final_str = temp_string
                    else:
                        final_str += temp_string
                
                if (start_to_cat_string==False):
                    #print 'final_str' + final_str                    
                    ary_refined_string[item_count] = final_str
                    final_str = ""
                    item_count+=1

            ary_refined_string[STOCK_ITEM.date] = str(year) + '-' + str(month).zfill(2) + '-' + str(day).zfill(2)
            for index in range(STOCK_ITEM.MA5, int(STOCK_ITEM.TOTAL_ITEMS)):
                ary_refined_string[index] = "0.0"

            fetch7.create_table_by_stockID(self, currentStockID)
            #print ary_refined_string[STOCK_ITEM.number]
            #print ary_refined_string[STOCK_ITEM.close_price]
            tempData = ary_refined_string[STOCK_ITEM.close_price]            
            try:
                float(tempData)
                #print 'digital data'
                ary_refined_string[STOCK_ITEM.MA5]   = self.calculate_MA(ary_refined_string[STOCK_ITEM.number], float(ary_refined_string[STOCK_ITEM.close_price]),   5, year, month, day)
                ary_refined_string[STOCK_ITEM.MA10]  = self.calculate_MA(ary_refined_string[STOCK_ITEM.number], float(ary_refined_string[STOCK_ITEM.close_price]),  10, year, month, day)
                ary_refined_string[STOCK_ITEM.MA20]  = self.calculate_MA(ary_refined_string[STOCK_ITEM.number], float(ary_refined_string[STOCK_ITEM.close_price]),  20, year, month, day)
                ary_refined_string[STOCK_ITEM.MA60]  = self.calculate_MA(ary_refined_string[STOCK_ITEM.number], float(ary_refined_string[STOCK_ITEM.close_price]),  60, year, month, day)
                ary_refined_string[STOCK_ITEM.MA120] = self.calculate_MA(ary_refined_string[STOCK_ITEM.number], float(ary_refined_string[STOCK_ITEM.close_price]), 120, year, month, day)
                ary_refined_string[STOCK_ITEM.MA240] = self.calculate_MA(ary_refined_string[STOCK_ITEM.number], float(ary_refined_string[STOCK_ITEM.close_price]), 240, year, month, day)
            except ValueError:
                #print tempData
                IsValidEntry = False

            #fetch7.create_table_by_stockID(self, currentStockID)
            command = 'INSERT INTO '+ table + ' VALUES ('
            for index in range(int(STOCK_ITEM.TOTAL_ITEMS)):
                if (index < int(STOCK_ITEM.TOTAL_ITEMS)-1):
                    command += '?,'
                else:
                    command += '?)'

            checkItemExistedCmd = 'SELECT * FROM ' + 'RawData' + str(currentStockID) + ' WHERE date = ' + '\'' + str(year) + '-' + str(month).zfill(2) + '-' + str(day).zfill(2) + '\''
            #print checkItemExistedCmd
            db.execute(checkItemExistedCmd)
            get_raw_item_data=db.fetchall()

            #print currentStockID
            if (len(get_raw_item_data)>0):
                #print 'Duplicate row'
                {}
            else:
                if (IsValidEntry):
                    db.execute(command, ary_refined_string)

        fp_today_data.close()
        conn.commit()

    def calculate_MA(self, stockID, todayPrice, period, year, month, day):
        global db
        totalValue = todayPrice
        #GetDBDataCmd = 'SELECT close_price FROM RawData' + str(stockID) + ' WHERE date < ' \
        #               + 'ORDER BY \'' + str(year) + '-' + str(month).zfill(2) + '-' + str(day).zfill(2) + '\''\
        #               + ' limit ' + str(period-1);
        #SELECT * FROM RawData1101 WHERE date < '2014-05-05' ORDER BY date DESC LIMIT 10;
        
        GetDBDataCmd = 'SELECT close_price FROM RawData' + str(stockID) + ' WHERE date < \'' \
                       + str(year) + '-' + str(month).zfill(2) + '-' + str(day).zfill(2) + '\'' \
                       ' ORDER BY date DESC LIMIT ' + str(period-1)
        
        #print GetDBDataCmd
        db.execute(GetDBDataCmd)
        #get_previous_price_data = db.fetchall()
        get_previous_price_data = db.fetchone()

        #print len(get_previous_price_data)
        dataCount = 1
        while get_previous_price_data is not None:
            tempData = str(get_previous_price_data[0])
            tempData = tempData.replace('(', '')
            tempData = tempData.replace(')', '')
            tempData = tempData.replace(',', '')
            tempData = tempData.replace('\'', '')
            #if (stockID == '1101'):
            #    print tempData
            totalValue += float(tempData)            
            dataCount += 1
            get_previous_price_data = db.fetchone()
            
        #for each_row_data in get_previous_price_data:
        #    totalValue += float(each_row_data)
        #    dataCount += 1

        #if (stockID == '1101'):
        #    print period
        #    print totalValue
        #    print dataCount
        #    print GetDBDataCmd
            
        return totalValue / float(dataCount)
        

    def import_data_to_database(self, year, month, day):
        localSavedFileName = 'A112' + str(year) + str(month).zfill(2) + str(day).zfill(2) + 'ALL_1.csv'
        fp_today_data = open(localSavedFileName, "r")
        ary_single_line = []
        ary_refined_string = [None] * 16
        
        while True:            
            line_data = fp_today_data.readline()
            if not line_data: break
            ary_single_line = line_data.split(',')
            #ary_refined_string = line_data.split(',')
            str_len = len(ary_single_line[0])

            if (str_len != 4):
                continue
             
            if (ary_single_line[0].isdigit() == False):
                continue
            
            ary_size = len(ary_single_line)
            #print ary_size
            

            start_to_cat_string = False
            final_str = ""
            item_count = 0;
            for index in range(ary_size):                
                temp_string = ary_single_line[index]
                temp_string = temp_string.replace(',', '')
                if '\"' in temp_string:
                    if (start_to_cat_string==True):
                        start_to_cat_string = False
                    else:
                        start_to_cat_string = True

                temp_string = temp_string.replace('\"', '')

                if (start_to_cat_string==True):
                    final_str += temp_string
                else:
                    if (len(final_str) == 0):
                        final_str = temp_string
                    else:
                        final_str += temp_string
                
                if (start_to_cat_string==False):
                    #print 'final_str' + final_str                    
                    ary_refined_string[item_count] = final_str
                    final_str = ""
                    item_count+=1

            command = 'INSERT INTO '+ table + ' VALUES ('
            for index in range(item_count):
                if (index < item_count-1):
                    command += '?,'
                else:
                    command += '?)'

            db.execute(command, ary_refined_string)            
            
        fp_today_data.close()
        conn.commit()

def main(argv=None):
    #reload(sys)
    #sys.setdefaultencoding('utf8')
    t = fetch7()  
    t.open_create_db('STOCK.db')
    current_year = 0
    current_month = 0
    curent_day = 0
    global csvFile
    
    for year_index in range(2004, 2015):
    #for year_index in range(2014, 2015):
        #print year_index
        for month_inde in range (1, 13):
        #for month_inde in range (9, 10):
            for day_index in range (1,32):
                t.fetch_stock_info_by_date(year_index, month_inde, day_index)
                print csvFileName
                statinfo = os.stat(csvFileName)
                if (statinfo.st_size > 4096):                
                    #t.create_table(year_index, month_inde, day_index)
                    #t.import_data_to_database(year_index, month_inde, day_index)
                    t.import_data_to_database_by_StockID(year_index, month_inde, day_index)
                    os.remove(csvFileName)
                else:
                    os.remove(csvFileName)
        
    #t.create_table(2014, 8, 28)
    #t.fetch_stock_info_by_date(2014, 8, 28)
    #t.import_data_to_database(2014, 8, 28)
    
    t.close_db()

if __name__ == '__main__':
    sys.exit(main())
