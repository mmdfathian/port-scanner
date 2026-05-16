import pytest
from unittest.mock import patch
import socket
from port_scanner.resolver import resolve_host


class TestResolveHost:
    def test_valid_domain(self):
        with patch("socket.gethostbyname", return_value="142.250.185.46"):
            ip = resolve_host("google.com")
        assert ip == "142.250.185.46"

    def test_ip_passthrough(self):
        with patch("socket.gethostbyname", return_value="192.168.1.1"):
            ip = resolve_host("192.168.1.1")
        assert ip == "192.168.1.1"

    def test_invalid_host_raises_value_error(self):
        with patch("socket.gethostbyname", side_effect=socket.gaierror("fail")):
            with pytest.raises(ValueError, match="resolve"):
                resolve_host("invalid.nonexistent.host")
