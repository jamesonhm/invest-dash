# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = "sqlite:///./scraper.db"

# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = declarative_base()


import sqlite3
import datetime

TICKER_EOD = "ticker_eod"

con = sqlite3.connect("../scraper.db")


def create_eod_table():
    try:
        with con:
            con.execute(f"CREATE TABLE {TICKER_EOD}(date TEXT, ticker TEXT, close NUMERIC, UNIQUE(date, ticker))")
    except sqlite3.OperationalError:
        print("ticker_eod already exists")

def drop_eod_table():
    try:
        with con:
            con.execute(f"DROP TABLE {TICKER_EOD}")
    except sqlite3.OperationalError:
        print("failed to drop table")

def add_ticker_eod(date: datetime.date, ticker: str, close: float):
    try:
        with con:
            con.execute(f"INSERT INTO {TICKER_EOD} (date, ticker, close) VALUES (?, ?, ?)", (date, ticker, close))
    except sqlite3.IntegrityError:
        print(f"date/ticker combo already exists: {date}, {ticker}")
    except sqlite3.DatabaseError:
        print(f"{date}: unable to add close data for ticker {ticker}, close: {close}")
        raise


def get_recent_eods():
    try:
        with con:
            result = con.execute(f"SELECT date, ticker, close FROM {TICKER_EOD} WHERE date > DATE() - 1").fetchall()
            return result
    except sqlite3.DatabaseError:
        raise

if __name__ == "__main__":
    # drop_eod_table()
    create_eod_table()

    tablenames = con.execute("SELECT name FROM sqlite_master").fetchall()
    tables = [tablename[0] for tablename in tablenames]
    assert f"{TICKER_EOD}" in tables

    today_eod = get_recent_eods()
    for row in today_eod:
        print(row)