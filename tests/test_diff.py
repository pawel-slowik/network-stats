from networkstats import compute_diff


def test_sent_and_received() -> None:
    previous = {
        "eth0": {
            "receive_bytes": 800,
            "transmit_bytes": 600,
        },
        "wlan0": {
            "receive_bytes": 20,
            "transmit_bytes": 10,
        },
    }
    current = {
        "eth0": {
            "receive_bytes": 1000,
            "transmit_bytes": 900,
        },
        "wlan0": {
            "receive_bytes": 65,
            "transmit_bytes": 50,
        },
    }
    diff = compute_diff(previous, current)
    expected = {
        "eth0": {
            "bytes_received": 200,
            "bytes_sent": 300,
        },
        "wlan0": {
            "bytes_received": 45,
            "bytes_sent": 40,
        },
    }
    assert diff == expected


def test_skips_interface_when_no_traffic() -> None:
    previous = {
        "eth0": {
            "receive_bytes": 800,
            "transmit_bytes": 600,
        },
        "wlan0": {
            "receive_bytes": 20,
            "transmit_bytes": 10,
        },
    }
    current = {
        "eth0": {
            "receive_bytes": 1000,
            "transmit_bytes": 900,
        },
        "wlan0": {
            "receive_bytes": 20,
            "transmit_bytes": 10,
        },
    }
    diff = compute_diff(previous, current)
    assert "eth0" in diff
    assert "wlan0" not in diff


def test_empty_when_no_traffic() -> None:
    previous = {
        "eth0": {
            "receive_bytes": 800,
            "transmit_bytes": 600,
        },
        "wlan0": {
            "receive_bytes": 20,
            "transmit_bytes": 10,
        },
    }
    current = previous
    diff = compute_diff(previous, current)
    assert not diff


def test_empty_with_traffic_on_separate_interfaces() -> None:
    previous = {
        "eth0": {
            "receive_bytes": 800,
            "transmit_bytes": 600,
        },
    }
    current = {
        "wlan0": {
            "receive_bytes": 65,
            "transmit_bytes": 50,
        },
    }
    diff = compute_diff(previous, current)
    assert not diff
