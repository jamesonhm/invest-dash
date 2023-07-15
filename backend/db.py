# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = "sqlite:///./scraper.db"

# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = declarative_base()


import sqlite3

con = sqlite3.connect("../scraper.db")


def create_eod_table():
    try:
        with con:
            con.execute("CREATE TABLE ticker_eod(date, ticker, close)")
    except sqlite3.OperationalError:
        print("ticker_eod already exists")

def get_recent_eods():
    try:
        with con:
            result = con.execute("SELECT date, ticker, close FROM ticker_eod WHERE date > DATE() - 1").fetchall()
            return result
    except sqlite3.DatabaseError:
        raise

# create_eod_table()

print(con.execute("SELECT name FROM sqlite_master").fetchall())
assert 'ticker_eod' in con.execute("SELECT name FROM sqlite_master WHERE name = 'ticker_eod'").fetchall()[0]

today_eod = get_recent_eods()
for row in today_eod:
    print(row)