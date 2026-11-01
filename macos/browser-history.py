import csv
import os
import sqlite3
import sys

# Not sure why Safari has its own epoch, but it does. Classic Apple. safari_epoch_offset = 978307200


def main():
    user = arg_parser()
    export_to_csv(user, safari)
    export_to_csv(user, chrome)
    export_to_csv(user, edge)


def arg_parser():
    if len(sys.argv) < 2:
        print(f"No user provided, running as {os.environ['USER']}")
        return os.environ["USER"]
    elif len(sys.argv) > 2:
        print(f"Too many cli arguments, running as {os.environ['USER']}")
        return os.environ["USER"]
    if os.path.isdir(f"/Users/{sys.argv[1]}"):
        print(f"Collecting Browser history for {sys.argv[1]}")
        return sys.argv[1]
    else:
        sys.exit("ERROR: Provided user doesn't exist. No history was collected.")


class safari:
    name = "safari"
    file_path = "Library/Safari/History.db"
    sql = """ 
        SELECT
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


class chrome:
    name = "chrome"
    file_path = "Library/Application Support/Google/Chrome/Default/History"
    sql = """
            SELECT
                datetime(
                    visits.visit_time/1000000-11644473600, 'unixepoch', 'localtime'
                ) as 'visit_time',
                urls.url,
                urls.title
            FROM
                visits INNER JOIN urls ON visits.url = urls.id
            WHERE
                visits.visit_duration > 0
            ORDER BY
                visit_time DESC
        """


class edge:
    name = "edge"
    file_path = "Library/Application Support/Microsoft Edge/Default/History"
    sql = """
            SELECT
                datetime(
                    visits.visit_time/1000000-11644473600, 'unixepoch', 'localtime'
                ) as 'visit_time',
                urls.url,
                urls.title
            FROM
                visits INNER JOIN urls ON visits.url = urls.id
            WHERE
                visits.visit_duration > 0
            ORDER BY
                visit_time DESC
        """


def export_to_csv(user, browser):
    user_history = f"/Users/{user}/" + browser.file_path
    conn = sqlite3.connect(user_history)
    cur = conn.cursor()
    browser_history = cur.execute(browser.sql)
    with open(f"/tmp/{browser.name}_history.csv", "w", newline="") as csv_file:
        writer = csv.writer(csv_file)

        # Write headers
        column_names = [desc[0] for desc in browser_history.description]

        writer.writerow(column_names)

        # Write data rows

        writer.writerows(browser_history)
    conn.close()


if __name__ == "__main__":
    main()
