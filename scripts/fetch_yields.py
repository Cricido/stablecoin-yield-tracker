import requests
import csv
from datetime import datetime

today = datetime.today().strftime('%Y-%m-%d')
rows = []

try:
    response = requests.get("https://yields.llama.fi/pools")  # nuova API corretta
    if response.status_code != 200:
        raise Exception(f"Errore HTTP {response.status_code}")

    data = response.json()

    # Filtro Morpho Steckhouse USDT
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
    print(f"[ERRORE] {e}")

# Scrive nel file CSV se ci sono righe valide
if rows:
    with open("data/yield_log.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(rows)
else:
    print("[INFO] Nessun dato Morpho valido trovato.")
