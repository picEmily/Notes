"""
file: test_solution.py
this file is the unit test for solution.py
"""
from solution import getExpirationDate


class TestClass:
    """This is the unit test for solution

    """

    def testNormal(self):
        date = [2018, 10, 1]
        assert getExpirationDate(date[0], date[1], date[2]) == [2018, 11, 1]

    def testNormal2(self):
        date = [2018, 10, 31]
        assert getExpirationDate(date[0], date[1], date[2]) == [2018, 11, 30]

    def testNonLeapFeb(self):
        date = [2019, 1, 31]
        assert getExpirationDate(date[0], date[1], date[2]) == [2019, 2, 28]

    def test(self):
        date = [2100, 1, 29]
        assert getExpirationDate(date[0], date[1], date[2]) == [2100, 2, 28]

    def testLeapFeb(self):
        date = [2020, 1, 31]
        assert getExpirationDate(date[0], date[1], date[2]) == [2020, 2, 29]

    def testLeapFeb2(self):
        date = [2020, 1, 29]
        assert getExpirationDate(date[0], date[1], date[2]) == [2020, 2, 29]

    def testNewYear(self):
        date = [2018, 12, 31]
        assert getExpirationDate(date[0], date[1], date[2]) == [2019, 1, 31]
