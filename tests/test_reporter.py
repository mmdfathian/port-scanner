import pytest
from unittest.mock import patch
from port_scanner.reporter import print_report


class TestPrintReport:
    def test_with_open_ports(self):
        """وقتی پورت باز وجود داره، جدول چاپ می‌شه."""
        open_ports = [
            {"port": 80, "service": "http"},
            {"port": 443, "service": "https"},
        ]
        with patch("port_scanner.reporter.console") as mock_console:
            print_report("google.com", "1.2.3.4", open_ports, 1, 1024, 2.5)
        assert mock_console.print.called

    def test_with_no_open_ports(self):
        """وقتی پورت بازی نیست، پیام مناسب چاپ می‌شه."""
        with patch("port_scanner.reporter.console") as mock_console:
            print_report("google.com", "1.2.3.4", [], 1, 1024, 1.0)
        assert mock_console.print.called

    def test_port_with_empty_service(self):
        """پورتی که سرویس نداره باید بدون خطا چاپ بشه."""
        open_ports = [{"port": 12345, "service": ""}]
        with patch("port_scanner.reporter.console"):
            print_report("192.168.1.1", "192.168.1.1", open_ports, 1, 65535, 5.0)

    def test_call_count_with_ports(self):
        """با پورت باز، console.print حداقل دو بار صدا زده می‌شه (panel + table)."""
        open_ports = [{"port": 22, "service": "ssh"}]
        with patch("port_scanner.reporter.console") as mock_console:
            print_report("host", "1.1.1.1", open_ports, 1, 100, 0.5)
        assert mock_console.print.call_count >= 2

    def test_call_count_without_ports(self):
        """بدون پورت باز، console.print حداقل دو بار صدا زده می‌شه (panel + panel خطا)."""
        with patch("port_scanner.reporter.console") as mock_console:
            print_report("host", "1.1.1.1", [], 1, 100, 0.5)
        assert mock_console.print.call_count >= 2
