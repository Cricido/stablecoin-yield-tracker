
import requests
import csv
from datetime import datetime

today = datetime.today().strftime('%Y-%m-%d')

# Morpho Steckhouse USDT su Ethereum
# Questa API è un placeholder: può cambiare se Morpho aggiorna l'infrastruttura
response = requests.get("https://api.llama.fi/yield/morpho")
data = response.json()

# Filtra solo Steckhouse USDT
entries = [
    entry for entry in data["data"]["projects"]
    if entry["project"] == "morpho"
]

rows = []

for entry in entries:
    for vault in entry.get("vaults", []):
        if "steckhouse" in vault["symbol"].lower() and vault["symbol"].endswith("USDT"):
            rows.append([
                today,
                "Morpho",
                "Ethereum",
                "USDT",
                round(vault.get("apy", 0) * 100, 2),
                int(vault.get("tvlUsd", 0)),
                "Steckhouse",
                "real APY"
            ])

# Scrive nel file CSV
with open("data/yield_log.csv", "a", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(rows)
