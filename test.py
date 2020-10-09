import unittest
import david_currency_check

from pandas import DataFrame

class TestCurrencyCheck(unittest.TestCase):

    def test_01_parameters_ok(self):
        status, df = david_currency_check.get_iis_shares(market='foreign', tickers=david_currency_check.tickers_foreign)
        self.assertEqual((status,
                          isinstance(df, DataFrame),
                          df.columns.tolist(),
                          df.SECID.values.tolist()
                          ),
                         (True,
                          True,
                          ['SECID', 'PREVPRICE', 'SECNAME', 'PREVDATE'],
                          sorted(david_currency_check.tickers_foreign),
                          ))

    def test_02_parameters_ok(self):
        status, df = david_currency_check.get_iis_shares(market='russian', tickers=david_currency_check.tickers_russian)
        self.assertEqual((status,
                          isinstance(df, DataFrame),
                          df.columns.tolist(),
                          df.SECID.values.tolist(),
                          ),
                         (True,
                          True,
                          ['SECID', 'PREVPRICE', 'SECNAME', 'PREVDATE'],
                          sorted(david_currency_check.tickers_russian),
                          ))

    def test_03_parameters_nok_wrong_combination(self):
        status, df = david_currency_check.get_iis_shares(market='russian', tickers=david_currency_check.tickers_foreign)
        self.assertEqual((status,
                          isinstance(df, DataFrame),
                          df.columns.tolist(),
                          df.SECID.values.tolist(),
                          ),
                         (True,
                          True,
                          ['SECID', 'PREVPRICE', 'SECNAME', 'PREVDATE'],
                          [],
                          ))

    def test_04_parameters_nok_wrong_combination(self):
        status, df = david_currency_check.get_iis_shares(market='foreign', tickers=david_currency_check.tickers_russian)
        self.assertEqual((status,
                          isinstance(df, DataFrame),
                          df.columns.tolist(),
                          df.SECID.values.tolist()
                          ),
                         (True,
                          True,
                          ['SECID', 'PREVPRICE', 'SECNAME', 'PREVDATE'],
                          [],
                          ))

    def test_05_parameters_nok_wrong_values(self):
        status, df = david_currency_check.get_iis_shares(market='wrong', tickers=david_currency_check.tickers_russian)
        self.assertEqual((status,
                          isinstance(df, DataFrame),
                          df.columns.tolist(),
                          df.SECID.values.tolist()
                          ),
                         (False,
                          True,
                          ['SECID', 'PREVPRICE', 'SECNAME', 'PREVDATE'],
                          [],
                          ))

    def test_06_parameters_nok_wrong_values(self):
        status, df = david_currency_check.get_iis_shares(market='foreign', tickers=['wrong'])
        self.assertEqual((status,
                          isinstance(df, DataFrame),
                          df.columns.tolist(),
                          df.SECID.values.tolist()
                          ),
                         (True,
                          True,
                          ['SECID', 'PREVPRICE', 'SECNAME', 'PREVDATE'],
                          [],
                          ))

    def test_07_parameters_nok_wrong_types(self):
        status, df = david_currency_check.get_iis_shares(market=666, tickers=david_currency_check.tickers_russian)
        self.assertEqual((status,
                          isinstance(df, DataFrame),
                          df.columns.tolist(),
                          df.SECID.values.tolist()
                          ),
                         (False,
                          True,
                          ['SECID', 'PREVPRICE', 'SECNAME', 'PREVDATE'],
                          [],
                          ))

    def test_08_parameters_nok_wrong_types(self):
        status, df = david_currency_check.get_iis_shares(market='foreign', tickers=666)
        self.assertEqual((status,
                          isinstance(df, DataFrame),
                          df.columns.tolist(),
                          df.SECID.values.tolist()
                          ),
                         (False,
                          True,
                          ['SECID', 'PREVPRICE', 'SECNAME', 'PREVDATE'],
                          [],
                          ))

if __name__ == '__main__':
    unittest.main(verbosity=2)

# status, df = david_currency_check.get_iis_shares(market='foreign', tickers=david_currency_check.tickers_foreign)
# print(df.sort_values(by='SECID'))
#
# status, df = david_currency_check.get_iis_shares(market='russian', tickers=david_currency_check.tickers_russian)
# print(df.sort_values(by='SECID'))
#
# david_currency_check.get_iis_shares()

# python test.py