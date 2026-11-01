import sqlite3
import csv
import time

safari_epoch_offset = 978307200
# getting safari logs
conn = sqlite3.connect("/Users/jmac/Library/Safari/History.db")
cur = conn.cursor()
safari_history = cur.execute(
    "SELECT hi.id, hi.url, hv.visit_time, hv.title FROM history_items hi JOIN history_visits hv on HI.id = hv.history_item WHERE hi.url IS NOT NULL ORDER BY hv.visit_time DESC"
)

# Adjusting Safari's 2001 epoch time first to the unix epoch for some common ground, then to human readable UTC.
safari_history_time_adjusted = []

for id, url, visit_time, title in safari_history:
    epoch_adjusted_time = visit_time + safari_epoch_offset
    human_date_time_utc = time.strftime(
        "%Y-%m-%d %H:%M:%S", time.gmtime(epoch_adjusted_time)
    )
    new_record = (url, human_date_time_utc, title)
    safari_history_time_adjusted.append(new_record)

with open("safari_history_original.csv", "w", newline="") as csv_file:
    writer = csv.writer(csv_file)

    # Write headers
    column_names = [desc[0] for desc in safari_history.description]

    writer.writerow(column_names)

    # Write data rows

    writer.writerows(safari_history)
conn.close()

with open("safari_history_adjusted.csv", "w", newline="") as csv_file:
    writer = csv.writer(csv_file)

    # Write headers
    column_names = [
        "url",
        "human_date_time_utc",
        "title",
    ]

    writer.writerow(column_names)

    # Write data rows

    writer.writerows(safari_history_time_adjusted)
