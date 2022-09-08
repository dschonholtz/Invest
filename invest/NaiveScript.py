"""
A simple script that iterates through the csv file: AllEtradeSymbolsSummary14082022.csv and
calls the dbInterface.py file to create a record with that symbols most rudimentary data in it.
"""

import csv
from sqlalchemy import asc
from requests import JSONDecodeError
from time import sleep

from dbInterface import Session, Base, engine
from models.EtradeData import EtradeSummary
from models.SAChartData import SAChartData
from SeekingAlphaApi import SeekingAlphaApi


def read_csv(file_name):
    """
    Reads the csv file and returns a list of dictionaries.
    :param file_name: The name of the csv file to read.
    :return: A list of dictionaries.
    """
    with open(file_name, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        return list(reader)


def insert_record(record, session):
    """
    Inserts a record into the postgres database using SQLAlchemy in the dbInterface.py file.
    :param record: The record to insert.
    :return: None.
    """
    # check if the symbol value is not alphanumeric or non empty
    if not record['Symbol'].isalnum() or record['Symbol'] == '':
        return
    # check if the record already exists in the database
    existing_record = session.query(EtradeSummary).filter_by(symbol=record['Symbol']).first()
    if existing_record:
        return
    summary_record = EtradeSummary(
        symbol=record['Symbol'],
        company_name=record['Company Name'],
        industry=record['Industry'],
        mkt_cap=record["Mkt Cap"]
    )
    session.add(summary_record)


def populate_sa_chart_iterator(query_result, session):
    should_retry = []
    for record in query_result:
        print(f'Processing {record.symbol}  {record.mkt_cap}')
        try:
            sa_chart_resp = SeekingAlphaApi().get_historical_chart(record.symbol)
        except JSONDecodeError as e:
            print(f'JSONDecodeError for {record.symbol}: {e}')
            continue
        except Exception as e:
            print(f'Exception for {record.symbol}: {e} will not retry')
            continue
        if not sa_chart_resp or not sa_chart_resp['attributes']:
            print(f'No valid chart data for {record.symbol}')
            should_retry.append(record)
            continue
        print(f'Storing data for {record.symbol}')
        sa_chart_data = SAChartData(record.symbol)
        existing_record = session.query(sa_chart_data.table).first()
        if existing_record:
            continue
        # Batch insert the values in teh sa_chart_data table from the response
        for date, values in sa_chart_resp['attributes'].items():
            # Check if the date is in the database, don't insert if the record exists
            existing_record = session.query(sa_chart_data.table).filter_by(date=date).first()
            if existing_record:
                continue
            if not values['volume']:
                values['volume'] = 0
            if 'percentChange' in values:
                values['percentChange'] = values['percentChange']
            else:
                values['percentChange'] = 0.0000000001
            sa_chart_data.insert(date, values['volume'], values['high'], values['close'], values['low'],
                                 values['open'], values['percentChange'])
        sleep(.2)

    return should_retry


def populate_sa_chart():
    # populate the sa_chart_data table
    session = Session()

    query_result = session.query(
        EtradeSummary
    ).order_by(
        asc(EtradeSummary.mkt_cap)
    ).where(EtradeSummary.mkt_cap > 365000000).all()
    should_retry = populate_sa_chart_iterator(query_result, session)
    populate_sa_chart_iterator(should_retry, session)
    session.commit()
    session.close()


def populate_etrade_summary():
    """
    The main function.
    :return: None.
    """
    # if there is no db we could create it.
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    session = Session()
    records = read_csv('AllEtradeSymbolsSummary14082022.csv')
    for record in records:
        insert_record(record, session)
    session.commit()
    query_result = session.query(EtradeSummary).all()
    # now print the query results
    for record in query_result:
        print(record.symbol, record.company_name, record.industry, record.mkt_cap)
    session.close()


def list_recs():
    # list all records in the database
    session = Session()
    query_result = session.query(EtradeSummary).all()
    # save all the query results to a file
    with open('query_results.txt', 'w') as f:
        for record in query_result:
            f.write(str(record.symbol) + ' ' + str(record.company_name) + ' ' + str(record.industry) + '\n')


if __name__ == '__main__':
    populate_sa_chart()
