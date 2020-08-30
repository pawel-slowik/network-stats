#!/usr/bin/env python3

import time
import sqlite3
from typing import Mapping

Stats = Mapping[str, Mapping[str, int]]
Diff = Mapping[str, Mapping[str, int]]


def read_stats() -> Stats:
    lines = open("/proc/net/dev").readlines()
    top_labels = [chunk.lower().strip() for chunk in lines[0].split("|")][1:]
    item_labels = [chunk.split() for chunk in lines[1].split("|")][1:]
    combined_labels = []
    for idx, top_label in enumerate(top_labels):
        for item_label in item_labels[idx]:
            combined_labels.append(top_label + "_" + item_label)
    data = {}
    for line in lines[2:]:
        parts = line.split()
        interface = parts[0].strip(":")
        numbers = [int(n) for n in parts[1:]]
        data[interface] = dict(zip(combined_labels, numbers))
    return data


def compute_diff(previous: Stats, current: Stats) -> Diff:
    diff = {}
    for interface, current_values in current.items():
        if interface not in previous:
            continue
        previous_values = previous[interface]
        received = current_values["receive_bytes"] - previous_values["receive_bytes"]
        sent = current_values["transmit_bytes"] - previous_values["transmit_bytes"]
        if received < 0 or sent < 0:
            continue
        if received == 0 and sent == 0:
            continue
        diff[interface] = {
            "bytes_received": received,
            "bytes_sent": sent,
        }
    return diff


def save_diff(filename: str, diff: Diff, previous_timestamp: float, timestamp: float) -> None:
    if not diff:
        return
    conn = sqlite3.connect(filename)
    cursor = conn.cursor()
    for interface, values in diff.items():
        entry = {
            "timestamp_begin": previous_timestamp,
            "timestamp_end": timestamp,
            "interface": interface,
            "bytes_sent": values["bytes_sent"],
            "bytes_received": values["bytes_received"],
        }
        query = "INSERT INTO traffic (%s) VALUES (%s)" % (
            ", ".join(entry.keys()),
            ", ".join(":" + key for key in entry),
        )
        cursor.execute(query, entry)
    conn.commit()
    conn.close()


def create_table(filename: str) -> None:
    sql = """
CREATE TABLE IF NOT EXISTS traffic (
	timestamp_begin INT NOT NULL,
	timestamp_end INT NOT NULL,
	interface VARCHAR NOT NULL,
	bytes_sent BIGINT NOT NULL,
	bytes_received BIGINT NOT NULL,
	PRIMARY KEY (timestamp_begin, timestamp_end, interface)
);
"""
    conn = sqlite3.connect(filename)
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    conn.close()


def main() -> None:
    import argparse
    import logging
    parser = argparse.ArgumentParser(
        description="Log Linux network traffic statistics into a SQLite database"
    )
    parser.add_argument("database", help="SQLite database file")
    parser.add_argument("-v", action="store_true", dest="verbose", help="increase verbosity")
    args = parser.parse_args()
    logging.basicConfig(
        format="%(asctime)s [%(levelname)s] %(message)s",
        level=logging.DEBUG if args.verbose else logging.WARN,
    )
    create_table(args.database)
    previous_timestamp = None
    previous_stats = None
    while True:
        timestamp = time.time()
        stats = read_stats()
        if previous_stats is not None:
            diff = compute_diff(previous_stats, stats)
            logging.debug(diff)
            save_diff(args.database, diff, previous_timestamp, timestamp)
        previous_stats = stats
        previous_timestamp = timestamp
        time.sleep(10)


if __name__ == "__main__":
    main()
