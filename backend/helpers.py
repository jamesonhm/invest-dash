from datetime import datetime


def ts_to_str(ts: float):
    return datetime.fromtimestamp(ts).strftime("%Y/%m/%d %H:%M:%S")


def score_round(score: float):
    return round(score or 0, 2)


if __name__ == "__main__":
    print(ts_to_str(1695758401))
