# *-* coding: UTF-8 *-*
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

def insert_into_role_numbers(
    role_number,
    school_name,
    address1,
    address2,
    address3,
    country,
    aDict):
    if get_role_number(role_number, aDict) is None:
        aDict.append(dict(zip(['role_number',
            'school_name',
            'address1',
            'address2',
            'address3',
            'country'],
            [role_number, school_name, address1, address2, address3, country])))


def get_role_number(role_number, aDict=role_numbers):
    return next((item for item in aDict if item['role_number'] == role_number),
        None)


insert_into_role_numbers('12345', 'Test1', '', '', '', '', role_numbers)
insert_into_role_numbers('23456', 'Test2', '', '', '', '', role_numbers)
insert_into_role_numbers('34567', 'Test3', '', '', '', '', role_numbers)
insert_into_role_numbers('45678', 'Test4', '', '', '', '', role_numbers)
insert_into_role_numbers('56789', 'Test5', '', '', '', '', role_numbers)

insert_into_role_numbers('12345A', 'Test1A', '', '', '', '', role_numbers)
insert_into_role_numbers('23456B', 'Test2B', '', '', '', '', role_numbers)
insert_into_role_numbers('34567C', 'Test3C', '', '', '', '', role_numbers)
insert_into_role_numbers('45678D', 'Test4D', '', '', '', '', role_numbers)
insert_into_role_numbers('56789E', 'Test5E', '', '', '', '', role_numbers)

insert_into_role_numbers('67890F', 'Test1F', '', '', '', '', role_numbers)
insert_into_role_numbers('78901G', 'Test2G', '', '', '', '', role_numbers)
insert_into_role_numbers('89012H', 'Test3H', '', '', '', '', role_numbers)
insert_into_role_numbers('90123I', 'Test4I', '', '', '', '', role_numbers)
insert_into_role_numbers('01234J', 'Test5J', '', '', '', '', role_numbers)

# note to self: put this in memcache!