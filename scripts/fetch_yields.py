# fetch_yields.py
# Placeholder script - in produzione collegherà le API/Subgraph per Morpho, Pendle, Yearn, Beefy, ecc.
import csv
from datetime import datetime

data = [
    [datetime.today().strftime('%Y-%m-%d'), "Morpho", "Ethereum", "USDT", 6.21, 8471235, "Steckhouse", "auto-compound"]
]

with open("data/yield_log.csv", "a", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(data)
