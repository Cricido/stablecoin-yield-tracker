import requests
import csv
from datetime import datetime

today = datetime.today().strftime('%Y-%m-%d')
rows = []

### ✅ 1. Morpho – Steckhouse USDT
try:
    response = requests.get("https://yields.llama.fi/pools")
    if response.status_code != 200:
        raise Exception(f"Errore HTTP Morpho: {response.status_code}")

    data = response.json()
    for entry in data.get("data", []):
        if (
            entry.get("project") == "morpho-blue"
            and "steckhouse" in entry.get("symbol", "").lower()
            and "usdt" in entry.get("symbol", "").lower()
        ):
            rows.append([
                today,
                "Morpho",
                entry.get("chain", "Ethereum"),
                "USDT",
                round(entry.get("apy", 0), 2),
                int(entry.get("tvlUsd", 0)),
                "Steckhouse",
                "real APY"
            ])
except Exception as e:
    print(f"[Morpho ERROR] {e}")

### ✅ 2. Pendle – YT su sUSDe, USDC, DAI...
try:
    for entry in data.get("data", []):  # riuso della stessa API
        if (
            entry.get("project") == "pendle"
            and entry.get("symbol", "").startswith("YT-")
            and any(stable in entry.get("symbol", "").upper() for stable in ["USDC", "DAI", "SUSDE"])
        ):
            symbol = entry["symbol"]
            token = (
                "sUSDe" if "SUSDE" in symbol.upper()
                else "USDC" if "USDC" in symbol.upper()
                else "DAI"
            )
            rows.append([
                today,
                "Pendle",
                entry.get("chain", "Ethereum"),
                token,
                round(entry.get("apy", 0), 2),
                int(entry.get("tvlUsd", 0)),
                symbol,
                "YT real APY"
            ])
except Exception as e:
    print(f"[Pendle ERROR] {e}")

### ✅ Scrittura finale solo se ci sono righe
if rows:
    with open("data/yield_log.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(rows)
    print(f"[INFO] {len(rows)} righe scritte nel CSV.")
else:
    print("[INFO] Nessun dato Morpho o Pendle valido oggi.")
