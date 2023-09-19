import datetime
import sqlite3


con = sqlite3.connect("./scraper.db", check_same_thread=False)


def dict_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}

con.row_factory = dict_factory

with con:
    con.execute("""
                CREATE TABLE IF NOT EXISTS ticker_eod (
                    date TEXT, 
                    ticker TEXT, 
                    close NUMERIC, 
                    UNIQUE(date, ticker)
                )
            """)

with con:
    con.execute("""
                CREATE TABLE IF NOT EXISTS ticker_history (
                    timestamp INTEGER, 
                    ticker TEXT, 
                    close NUMERIC, 
                    sroc NUMERIC,
                    UNIQUE(timestamp, ticker)
                )
            """)


def drop_eod_table():
    try:
        with con:
            con.execute(f"DROP TABLE ticker_eod")
    except sqlite3.OperationalError:
        print("failed to drop table")

def add_ticker_eod(date: datetime.date, ticker: str, close: float):
    try:
        with con:
            con.execute(f"INSERT INTO ticker_eod (date, ticker, close) VALUES (?, ?, ?)", (date, ticker, close))
    except sqlite3.IntegrityError:
        print(f"date/ticker combo already exists: {date}, {ticker}")
    except sqlite3.DatabaseError:
        print(f"{date}: unable to add close data for ticker {ticker}, close: {close}")
        raise

def get_recent_eods():
    try:
        with con:
            result = con.execute(f"SELECT date, ticker, close FROM ticker_eod WHERE date > DATE() - 1").fetchall()
            return result
    except sqlite3.DatabaseError:
        raise

def get_ticker_eods():
    try:
        with con:
            result = con.execute(f"""
            SELECT date, 
                   ticker, 
                   close
              FROM ticker_eod
          ORDER BY ticker
                  ,date
            """).fetchall()
            return result
    except sqlite3.DatabaseError:
        raise

def get_ticker(symbol: str) -> list[dict]:
    try:
        with con:
            result = con.execute(f"""
            SELECT timestamp,  
                   close
              FROM ticker_history
             WHERE ticker = ?
          ORDER BY timestamp
            """, [symbol]).fetchall()
            return result
    except sqlite3.DatabaseError:
        raise

def get_ticker_latest(symbol:str) -> list[dict]:
    with con:
        result = con.execute(f"""
        SELECT max(timestamp) latest,  
                count(timestamp) daycount
            FROM ticker_history
            WHERE ticker = ?
        """, [symbol]).fetchall()
        return result


def update_history(ticker: str, timestamp: int, close: float) -> int:
    with con:
        result = con.execute(""" 
            INSERT INTO ticker_history (
                        timestamp,
                        ticker,
                        close) 
                 VALUES (?, ?, ?) 
            ON CONFLICT (timestamp, ticker) DO NOTHING
        """, [timestamp, ticker, close])
        return result

def update_history_many(data: list[tuple]) -> int:
    with con:
        result = con.executemany(""" 
            INSERT INTO ticker_history (
                        timestamp,
                        ticker,
                        close) 
                 VALUES (?, ?, ?) 
            ON CONFLICT (timestamp, ticker) DO NOTHING
        """, data)
        return result

def update_ticker_sroc(ticker: str, ts: int, sroc: float) -> int:
    with con:
        result = con.execute("""
            UPDATE ticker_history
               SET sroc = ?
             WHERE timestamp = ?
               AND ticker = ?
        """, sroc, ts, ticker)
        return result

if __name__ == "__main__":
    # drop_eod_table()
    # create_eod_table()

    # tablenames = con.execute("SELECT name FROM sqlite_master").fetchall()
    # print(tablenames)
    # if len(tablenames):
    #     assert f"ticker_eod" in [table["name"] for table in tablenames]
    # else:
    #     print("No tables exist")

    # eods = get_ticker_eods()
    # for d in eods:
    #     print(d)

    aapl = get_ticker("AAPL")
    print(aapl)

    # # print(today_eod[0][0])
    # for row in today_eod[0]:
    #     print(row)