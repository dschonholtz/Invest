from dbInterface import Base, engine
from sqlalchemy import Column, BigInteger, MetaData, Table, DateTime, Float


class SAChartData:
    """
    A SQL Table for the e-trade summary data of ~8000 stocks
    """

    def __init__(self, symbol):
        metadata_obj = MetaData()

        self.table = Table(f'{symbol}_chart', metadata_obj,
                           Column('date', DateTime, primary_key=True),
                           Column('volume', BigInteger, nullable=False),
                           Column('high', Float, nullable=False),
                           Column('close', Float, nullable=False),
                           Column('low', Float, nullable=False),
                           Column('open', Float, nullable=False),
                           Column('percent_change', Float, nullable=False),
                           )

        metadata_obj.create_all(engine)

    def insert(self, date, volume, high, day_close, low, day_open, percent_change):
        """
        Inserts a record into this objects table.
        :param date: The date of the record.
        :param volume: The volume of the record.
        :param high: The high of the record.
        :param day_close: The close of the record.
        :param low: The low of the record.
        :param day_open: The open of the record.
        :param percent_change: The percent change of the record.
        :return: None.
        """
        record = self.table.insert().values(
            date=date, volume=volume, high=high, close=day_close, low=low,
            open=day_open, percent_change=percent_change)
        engine.execute(record)
