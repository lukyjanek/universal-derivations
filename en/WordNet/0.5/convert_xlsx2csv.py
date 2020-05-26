#!/usr/bin/env python3
# coding: utf-8

"""Convert .xlsx to .csv."""

import csv
import xlrd
import argparse


# parse input parameters
parser = argparse.ArgumentParser()
parser.add_argument('-i', action='store', dest='i', required=True,
                    help='path to the .xlsx file')
parser.add_argument('-o', action='store', dest='o', required=True,
                    help='path to the output .csv file')
par = parser.parse_args()


# convert
wb = xlrd.open_workbook(par.i)
sh = wb.sheet_by_name('Sheet1')
your_csv_file = open(par.o, 'w')
wr = csv.writer(your_csv_file, quoting=csv.QUOTE_ALL)

for rownum in range(sh.nrows):
    wr.writerow(sh.row_values(rownum))

your_csv_file.close()
