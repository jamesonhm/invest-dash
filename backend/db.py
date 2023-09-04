import datetime
import sqlite3

TICKER_EOD = "ticker_eod"

con = sqlite3.connect("./scraper.db", check_same_thread=False)


def dict_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}

con.row_factory = dict_factory

with con:
    con.execute(f"""
                CREATE TABLE IF NOT EXISTS {TICKER_EOD} (
                    date TEXT, 
                    ticker TEXT, 
                    close NUMERIC, 
                    UNIQUE(date, ticker)
                )
            """)
    

# def create_eod_table():
#     try:
#         with con:
#             con.execute(f"CREATE TABLE {TICKER_EOD}(date TEXT, ticker TEXT, close NUMERIC, UNIQUE(date, ticker))")
#     except sqlite3.OperationalError:
#         print("ticker_eod already exists")

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

def get_ticker_eods():
    try:
        with con:
            result = con.execute(f"""
            SELECT 
                date, 
                ticker, 
                close
            FROM 
                {TICKER_EOD}
            ORDER BY 
                date, 
                ticker
            """).fetchall()
            return result
    except sqlite3.DatabaseError:
        raise

# def get_ticker_eods():
#     try:
#         with con:
#             result = con.execute(f"""SELECT json_group_array(
#                 json_object(
#                     'date', date, 
#                     'ticker', ticker, 
#                     'close', close
#                     )
#                 ) FROM {TICKER_EOD}
#             """).fetchall()
#             return result
#     except sqlite3.DatabaseError:
#         raise



if __name__ == "__main__":
    # drop_eod_table()
    # create_eod_table()

    tablenames = con.execute("SELECT name FROM sqlite_master").fetchall()
    print(tablenames)
    if len(tablenames):
        assert f"{TICKER_EOD}" in [table["name"] for table in tablenames]
    else:
        print("No tables exist")

    eods = get_ticker_eods()
    print(eods)
    print(type(eods))
    # # print(today_eod[0][0])
    # for row in today_eod[0]:
    #     print(row)