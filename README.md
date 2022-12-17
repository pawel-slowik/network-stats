![Build Status][build-badge]
[build-badge]: https://github.com/pawel-slowik/network-stats/workflows/tests/badge.svg

This script periodically reads Linux network traffic statistics from
`/proc/net/dev` and saves the data into a SQLite database.

## Installation

There is no installation script yet. Just copy the `networkstats.py` file into
`/usr/local/bin` or wherever you want it. The script requires Python 3.x to run.
Only the Python standard library is required, there's no need to install any
additional modules.

## Usage

Run:

	/usr/local/bin/networkstats.py /path/networkstats.db

Run with `--help` for a list of options.

### Running as a system wide daemon

The script intentionally does not behave like a Unix daemon, because:

1. implementing correct daemon behaviour is complicated and
2. there are wrappers and other tools that add that functionality.

For example, you could use [daemonize](http://software.clapper.org/daemonize/)
like this:

	daemonize \
	-p /var/run/network-stats.pid \
	-l /var/lock/network-stats.lock \
	-u network-stats \
	/usr/local/bin/networkstats.py /var/db/network-stats/network-stats.db

### Displaying statistics

Take a look at the example queries in `examples/*.sql` files. Enter queries at
the SQLite console, e.g.:

	$ sqlite3 -header -column /var/db/network-stats/network-stats.db

	sqlite> .read examples/last_week.sql

	week_date   traffic_MiB
	----------  -----------
	2019-01-11  220
	2019-01-12  757
	2019-01-13  552
	2019-01-14  950
	2019-01-15  337
	2019-01-16  214
	2019-01-17  386
