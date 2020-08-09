"""
file: solution.py
this file compute the expire date of the input date
"""


def getExpirationDate(year, month, day):
    """ 假设year，month，day是正确整数日期;订购时长一个月
    params:
        year: integer
        month: an integer from 1 to 12
        day: an integer from 1 to 32
    return:
        list [year, month, day]
    """

    # 储存每个月对应的最大天数
    daysOfMonthNonleap = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    daysOfMonthLeap = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    # 得到月和年
    month += 1
    if month == 13:
        month = 1
        year += 1

    # 判断是否为闰年,得到每个月的天数
    daysOfMonth = daysOfMonthNonleap
    if isLeap(year):
        daysOfMonth = daysOfMonthLeap

    # 判断日期
    if day > daysOfMonth[month - 1]:
        day = daysOfMonth[month - 1]

    return [year, month, day]


def isLeap(year):
    """判断是否为闰年
    params:
        year: integer
    return:
        boolean
    """
    if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
        return True
    return False
