#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2011
# Free Software Foundation, Inc.
#
# This file is part of the gtk-fortran gtk+ Fortran Interface library.
#
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# Under Section 7 of GPL version 3, you are granted additional
# permissions described in the GCC Runtime Library Exception, version
# 3.1, as published by the Free Software Foundation.
#
# You should have received a copy of the GNU General Public License along with
# this program; see the files COPYING3 and COPYING.RUNTIME respectively.
# If not, see <http://www.gnu.org/licenses/>.
#
# Contributed by Vincent Magnin, 04.04.2011, Python 2.6.6, Linux Ubuntu 10.10
# Last modification: 04.04.2011

""" This program helps you generating the USE statements for your gtk-fortran programs.
Command line: python usemodules.py directorytoscan/
"""

import os
import csv
import sys

def multiline(ch, maxlength):
    """Split a long line in a multiline, following Fortran syntax."""
    result = ""
    while len(ch) > maxlength-1:
        result += ch[0:maxlength-1] + "&\n"
        ch = "&"+ ch[maxlength-1:]
    result += ch
    return result


output_file = open("usemodules.txt", "w")
header = """Generated by usemodules.py
Note that you should adapt these USE statements to each scoping unit.
The script just identifies all the functions used in a given file.
You should also add enums identifiers and parameters.
\n
"""
output_file.write(header)

used_functions = []

# All Fortran files in this directory and its subdirectories:
path = sys.argv[1] #"../examples/"
if not path.endswith("/"):
    path += "/" # Will not work with MS Windows
    
tree = os.walk(path)
for directory in tree:
    for f_name in directory[2]:
        if f_name.find("-auto") != -1:
            continue  # Next file
        
        if f_name.endswith(".f90") or f_name.endswith(".f95") or f_name.endswith(".f03") or f_name.endswith(".f08"):
            print f_name
            only_dict = {}
            used_modules = []
            # FIXME: / will not work with Windows:
            whole_file = open(directory[0] + "/" + f_name, 'rU').read()

            # Loading the GTK+ functions index generated by cfwrapper.py:
            reader = csv.reader(open("gtk-fortran-index.csv", "r"), delimiter=";")
            for row in reader:
                module_name = row[0]
                function_name = row[1]
                if whole_file.find(function_name) != -1:
                    if not module_name in used_modules:
                        used_modules.append(module_name)
                        only_dict[module_name] = "use "+module_name+", only: "
                    only_dict[module_name] += function_name + ", "
                    if not function_name in used_functions:
                        used_functions.append(function_name)

            output_file.write(f_name+"\n"+"============\n")
            for key in only_dict.keys():
                output_file.write(multiline(only_dict[key].rstrip(", "), 80)+"\n")
            output_file.write("\n\n")

output_file.close()

used_functions.sort()
print used_functions
