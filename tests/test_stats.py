# pylint: disable=line-too-long
from networkstats import parse_stats


def test_parse_stats() -> None:
    lines = [
        "Inter-|   Receive                                                |  Transmit",
        " face |bytes    packets errs drop fifo frame compressed multicast|bytes    packets errs drop fifo colls carrier compressed",
        "    lo: 5017768   46560    0    0    0     0          0         0  5017768   46560    0    0    0     0       0          0",
        "  eth0:       0       0    0    0    0     0          0         0        0       0    0    0    0     0       0          0",
        "  eth1:       0       0    0    0    0     0          0         0        0       0    0    0    0     0       0          0",
        " wlan0: 76844384   67182    0    0    0     0          0         0  4998547   33420    0    0    0     0       0          0",
    ]
    stats = parse_stats(lines)
    expected = {
        'eth0': {
            'receive_bytes': 0,
            'receive_compressed': 0,
            'receive_drop': 0,
            'receive_errs': 0,
            'receive_fifo': 0,
            'receive_frame': 0,
            'receive_multicast': 0,
            'receive_packets': 0,
            'transmit_bytes': 0,
            'transmit_carrier': 0,
            'transmit_colls': 0,
            'transmit_compressed': 0,
            'transmit_drop': 0,
            'transmit_errs': 0,
            'transmit_fifo': 0,
            'transmit_packets': 0,
        },
        'eth1': {
            'receive_bytes': 0,
            'receive_compressed': 0,
            'receive_drop': 0,
            'receive_errs': 0,
            'receive_fifo': 0,
            'receive_frame': 0,
            'receive_multicast': 0,
            'receive_packets': 0,
            'transmit_bytes': 0,
            'transmit_carrier': 0,
            'transmit_colls': 0,
            'transmit_compressed': 0,
            'transmit_drop': 0,
            'transmit_errs': 0,
            'transmit_fifo': 0,
            'transmit_packets': 0,
        },
        'lo': {
            'receive_bytes': 5017768,
            'receive_compressed': 0,
            'receive_drop': 0,
            'receive_errs': 0,
            'receive_fifo': 0,
            'receive_frame': 0,
            'receive_multicast': 0,
            'receive_packets': 46560,
            'transmit_bytes': 5017768,
            'transmit_carrier': 0,
            'transmit_colls': 0,
            'transmit_compressed': 0,
            'transmit_drop': 0,
            'transmit_errs': 0,
            'transmit_fifo': 0,
            'transmit_packets': 46560,
        },
        'wlan0': {
            'receive_bytes': 76844384,
            'receive_compressed': 0,
            'receive_drop': 0,
            'receive_errs': 0,
            'receive_fifo': 0,
            'receive_frame': 0,
            'receive_multicast': 0,
            'receive_packets': 67182,
            'transmit_bytes': 4998547,
            'transmit_carrier': 0,
            'transmit_colls': 0,
            'transmit_compressed': 0,
            'transmit_drop': 0,
            'transmit_errs': 0,
            'transmit_fifo': 0,
            'transmit_packets': 33420,
        },
    }
    assert stats == expected