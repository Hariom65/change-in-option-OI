import os
import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from nsepython import *

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

data = nse_optionchain_scrapper("NIFTY")

records = data["filtered"]["data"]

ce_total = 0
pe_total = 0

for item in records:

    if item.get('CE'):
        ce_total += item['CE'].get('changeinOpenInterest', 0)

    if item.get('PE'):
        pe_total += item['PE'].get('changeinOpenInterest', 0)

now = datetime.now().strftime("%H:%M")

new_row = pd.DataFrame([{
    "time": now,
    "ce_oi": ce_total,
    "pe_oi": pe_total
}])

csv_file = "oi_data.csv"

try:
    old_data = pd.read_csv(csv_file)
    data_df = pd.concat([old_data, new_row], ignore_index=True)
except:
    data_df = new_row

data_df.to_csv(csv_file, index=False)

plt.figure(figsize=(10,5))

plt.plot(data_df['time'], data_df['ce_oi'], label='CE OI')
plt.plot(data_df['time'], data_df['pe_oi'], label='PE OI')

plt.xticks(rotation=45)

plt.legend()

plt.title("NIFTY OI Trend")

graph_file = "oi_graph.png"

plt.savefig(graph_file)

message = f"""
NIFTY OI UPDATE

Time: {now}

Total CE OI Change: {ce_total}
Total PE OI Change: {pe_total}
"""

telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"

with open(graph_file, "rb") as photo:

    requests.post(
        telegram_url,
        data={
            "chat_id": CHAT_ID,
            "caption": message
        },
        files={
            "photo": photo
        }
    )

print("Graph sent successfully")
