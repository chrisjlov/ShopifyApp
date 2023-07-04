## ---------------------------
##
## Script name: convert_time.py
##
## Purpose of script: Converts dates into UTC format
##
## Author: Chris Lovett
##
## Date Created: 2022-10-30
##
## Copyright (c) Chris Lovett, 2022
##
## ---------------------------

from datetime import datetime
import pytz

format  = "%Y-%m-%d %H:%M:%S"

def convert_to_UTC(date1, date2):
    """
    Convert given dates to UTC timezone

    Args:
        date1 (datetime.date): First date to convert
        date2 (datetime.date): Second date to convert

    Returns:
        tuple: Tuple containing the two dates in UTC timezone and in the format "%Y-%m-%d %H:%M:%S"
    """

    dt_str1  = datetime.combine(date1, datetime.min.time())
    dt_str1 = dt_str1.strftime(format)

    dt_str2  = datetime.combine(date2, datetime.max.time())
    dt_str2 = dt_str2.strftime(format)

    #========================================
    #============= First Date ===============
    #========================================

    # Create datetime object in local timezone
    local_dt1 = datetime.strptime(dt_str1, format)
    # print('Datetime in Local Time zone: ', local_dt1)

    # Convert local datetime to UTC time-zone datetime
    dt_utc1 = local_dt1.astimezone(pytz.UTC)
    # print('Datetime in UTC Time zone: ', dt_utc1)

    dt_utc_str1 = dt_utc1.strftime(format)
    # print('Datetime string in UTC Time zone: ', dt_utc_str1)


    #========================================
    #============ Second Date ===============
    #========================================

    # Create datetime object in local timezone
    local_dt2 = datetime.strptime(dt_str2, format)
    # print('Datetime in Local Time zone: ', local_dt2)

    # Convert local datetime to UTC time-zone datetime
    dt_utc2 = local_dt2.astimezone(pytz.UTC)
    #print('Datetime in UTC Time zone: ', dt_utc2)

    dt_utc_str2 = dt_utc2.strftime(format)
    # print('Datetime string in UTC Time zone: ', dt_utc_str2)

    return(dt_utc_str1, dt_utc_str2)

def convert_to_format(date1,date2):
    """
    Convert given dates to the format "%Y-%m-%d"

    Args:
        date1 (datetime.date): First date to convert
        date2 (datetime.date): Second date to convert

    Returns:
        tuple: Tuple containing the two dates in the format "%Y-%m-%d"
    """

    formatYMD  = "%Y-%m-%d"
    dt_str1  = datetime.combine(date1, datetime.min.time())
    dt_str1 = dt_str1.strftime(formatYMD)

    dt_str2  = datetime.combine(date2, datetime.max.time())
    dt_str2 = dt_str2.strftime(formatYMD)

    return(dt_str1, dt_str2)
