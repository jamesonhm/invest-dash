import datetime
import sqlite3


con = sqlite3.connect("./scraper.db", check_same_thread=False)


def dict_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}

con.row_factory = dict_factory


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

def drop_table(name: str):
    try:
        with con:
            con.execute(f"DROP TABLE {name}")
    except sqlite3.OperationalError:
        print("failed to drop table")

def get_recent_eods():
    try:
        with con:
            result = con.execute("""
                SELECT date, 
                       ticker, 
                       close 
                  FROM ticker_history
                 WHERE date > DATE() - 1
            """).fetchall()
            return result
    except sqlite3.DatabaseError:
        raise

def get_ticker_eods():
    try:
        with con:
            result = con.execute("""
            SELECT date, 
                   ticker, 
                   close
              FROM ticker_history
          ORDER BY ticker
                  ,date
            """).fetchall()
            return result
    except sqlite3.DatabaseError:
        raise

def get_ticker(symbol: str) -> list[dict]:
    try:
        with con:
            result = con.execute("""
            SELECT timestamp,  
                   close
              FROM ticker_history
             WHERE ticker = ?
          ORDER BY timestamp
            """, [symbol]).fetchall()
            return result
    except sqlite3.DatabaseError:
        raise

def get_ticker_sroc(symbol: str) -> list[dict]:
    try:
        with con:
            result = con.execute("""
            SELECT timestamp,  
                   sroc
              FROM ticker_history
             WHERE ticker = ?
          ORDER BY timestamp
            """, [symbol]).fetchall()
            return result
    except sqlite3.DatabaseError:
        raise

def get_latest_scores() -> list[dict]:
    try:
        with con:
            result = con.execute("""
            SELECT max(timestamp)
                   ,ticker 
                   ,sroc
              FROM ticker_history
          GROUP BY ticker
            """, [symbol]).fetchall()
            return result
    except sqlite3.DatabaseError:
        raise

def get_ticker_latest(symbol:str) -> list[dict]:
    with con:
        result = con.execute("""
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

def update_close_many(data: list[tuple]) -> int:
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
        """, [sroc, ts, ticker])
        return result

def update_sroc_many(data: list[dict]) -> int:
    with con:
        result = con.executemany(""" 
            UPDATE ticker_history 
               SET sroc = :sroc
             WHERE timestamp = :timestamp
               AND ticker = :ticker
        """, data)
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