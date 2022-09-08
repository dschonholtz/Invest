"""
Tests the seeking alpha api class
"""
from invest.SeekingAlphaApi import SeekingAlphaApi


def test_bad_symbol():
    data = SeekingAlphaApi().get_historical_chart("BADSYMBOL")
    assert data == {}


def test_good_symbol():
    data = SeekingAlphaApi().get_historical_chart("AAPL")
    print(data)
    assert data['attributes'] != {}
