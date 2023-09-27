from datetime import datetime


def ts_to_str(ts: float):
    return datetime.fromtimestamp(ts)


if __name__ == "__main__":
    print(ts_to_str(1695758401))
