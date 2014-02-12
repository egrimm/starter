#-------------------------------------------------------------------------------
# Name:        role_numbers
# Purpose:     contains a dictionary of valid role numbers and other info
#
# Author:      egrimm
#
# Created:     23/01/2014
# Copyright:   (c) egrimm 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from collections import defaultdict

role_numbers = []

def insert_into_role_numbers(role_number, school_name, aDict):
    if get_role_number(role_number, aDict) is None:
        aDict.append(dict(zip(['role_number', 'school_name'],
            [role_number, school_name])))


def get_role_number(role_number, aDict=role_numbers):
    return next((item for item in aDict if item['role_number'] == role_number),
        None)


insert_into_role_numbers('12345', 'Countrywood', role_numbers)
insert_into_role_numbers('23456', 'Maplewood', role_numbers)
insert_into_role_numbers('34567', 'Silas Wood', role_numbers)
insert_into_role_numbers('45678', 'Stimson', role_numbers)
insert_into_role_numbers('56789', 'Huntington HS', role_numbers)
