import pytest
from unittest.mock import patch, MagicMock
from port_scanner.scanner import scan_port, scan


class TestScanPort:
    def test_open_port_returns_true(self):
        with patch("socket.socket") as mock_sock:
            instance = mock_sock.return_value.__enter__.return_value
            instance.connect_ex.return_value = 0
            with patch("socket.getservbyport", return_value="http"):
                port, is_open, service = scan_port("127.0.0.1", 80)
        assert is_open is True
        assert port == 80
        assert service == "http"

    def test_closed_port_returns_false(self):
        with patch("socket.socket") as mock_sock:
            instance = mock_sock.return_value.__enter__.return_value
            instance.connect_ex.return_value = 1
            port, is_open, service = scan_port("127.0.0.1", 9999)
        assert is_open is False
        assert service == ""

    def test_unknown_service(self):
        with patch("socket.socket") as mock_sock:
            instance = mock_sock.return_value.__enter__.return_value
            instance.connect_ex.return_value = 0
            with patch("socket.getservbyport", side_effect=OSError):
                port, is_open, service = scan_port("127.0.0.1", 12345)
        assert is_open is True
        assert service == "unknown"

    def test_socket_error_returns_closed(self):
        import socket
        with patch("socket.socket") as mock_sock:
            mock_sock.return_value.__enter__.side_effect = socket.error
            port, is_open, service = scan_port("127.0.0.1", 80)
        assert is_open is False


class TestScan:
    def test_returns_sorted_open_ports(self):
        def fake_scan_port(host, port, timeout):
            return (port, port in [22, 80, 443], "http" if port == 80 else "ssh")

        with patch("port_scanner.scanner.scan_port", side_effect=fake_scan_port):
            results = scan("127.0.0.1", start_port=1, end_port=500)

        ports = [r["port"] for r in results]
        assert ports == sorted(ports)
        assert any(r["port"] == 80 for r in results)

    def test_no_open_ports_returns_empty(self):
        with patch("port_scanner.scanner.scan_port", return_value=(80, False, "")):
            results = scan("127.0.0.1", start_port=80, end_port=80)
        assert results == []
