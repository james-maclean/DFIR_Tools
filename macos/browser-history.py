import csv
import sqlite3

# safari_epoch_offset = 978307200
# getting safari logs
conn = sqlite3.connect("/Users/jmac/Library/Safari/History.db")
cur = conn.cursor()
safari_history = cur.execute(
    """ SELECT
            datetime(
                visit_time + 978307200, 'unixepoch', 'localtime'
            ) as visit_time,
            url,
            title
        FROM
            history_visits
        INNER JOIN
            history_items
        ON
            history_items.id = history_visits.history_item
        ORDER BY
            visit_time DESC
            """
)


def export_to_csv(browser, db_connection):
    with open(f"{browser}_history.csv", "w", newline="") as csv_file:
        writer = csv.writer(csv_file)

        # Write headers
        column_names = [desc[0] for desc in db_connection.description]

        writer.writerow(column_names)

        # Write data rows

        writer.writerows(db_connection)
    conn.close()


export_to_csv("safari", safari_history)
