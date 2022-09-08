from dbInterface import Base
from sqlalchemy import Column, String, BigInteger


class EtradeSummary(Base):
    """
    A SQL Table for the e-trade summary data of ~8000 stocks
    """
    __tablename__ = 'etrade_summary'
    symbol = Column(String, primary_key=True)
    company_name = Column(String)
    industry = Column(String)
    mkt_cap = Column(BigInteger)

    def __init__(self, symbol, company_name, industry, mkt_cap):
        self.symbol = symbol
        self.company_name = company_name
        self.industry = industry
        # get the number value in the string and cast it to a float
        mkt_cap_num = float(mkt_cap[1:-1])
        mkt_cap_unit = mkt_cap[-1]
        if mkt_cap_unit == 'B':
            mkt_cap_num *= 1000000000
        elif mkt_cap_unit == 'M':
            mkt_cap_num *= 1000000
        elif mkt_cap_unit == 'T':
            mkt_cap_num *= 1000000000000
        else:
            raise ValueError(f'Invalid mkt_cap_unit: {mkt_cap_unit}')
        self.mkt_cap = mkt_cap_num

