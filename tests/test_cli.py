import json
import pytest
from unittest.mock import patch
from port_scanner.cli import build_parser, output_json


class TestBuildParser:
    def test_defaults(self):
        """مقادیر پیش‌فرض parser درست هستن."""
        parser = build_parser()
        args = parser.parse_args(["google.com"])
        assert args.host == "google.com"
        assert args.start == 1
        assert args.end == 1024
        assert args.timeout == 1.0
        assert args.workers == 100
        assert args.output == "text"
        assert args.save is None

    def test_custom_range(self):
        """محدوده سفارشی درست parse می‌شه."""
        parser = build_parser()
        args = parser.parse_args(["host", "-s", "80", "-e", "443"])
        assert args.start == 80
        assert args.end == 443

    def test_json_output_flag(self):
        """فلگ --output json درست parse می‌شه."""
        parser = build_parser()
        args = parser.parse_args(["host", "--output", "json"])
        assert args.output == "json"

    def test_save_flag(self):
        """فلگ --save درست parse می‌شه."""
        parser = build_parser()
        args = parser.parse_args(["host", "--output", "json", "--save", "out.json"])
        assert args.save == "out.json"

    def test_invalid_output_choice(self):
        """مقدار نامعتبر برای --output خطا می‌ده."""
        parser = build_parser()
        with pytest.raises(SystemExit):
            parser.parse_args(["host", "--output", "xml"])


class TestOutputJson:
    def test_prints_valid_json(self, capsys):
        """خروجی JSON معتبر چاپ می‌شه."""
        open_ports = [{"port": 80, "service": "http"}]
        output_json("google.com", "1.2.3.4", open_ports, 1, 1024, 2.5, None)
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert data["host"] == "google.com"
        assert data["ip"] == "1.2.3.4"
        assert data["open_ports_count"] == 1
        assert data["open_ports"][0]["port"] == 80

    def test_json_structure(self, capsys):
        """ساختار JSON همه فیلدهای لازم رو داره."""
        output_json("host", "1.1.1.1", [], 1, 100, 1.0, None)
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert "host" in data
        assert "ip" in data
        assert "range" in data
        assert "duration_seconds" in data
        assert "open_ports_count" in data
        assert "open_ports" in data

    def test_saves_to_file(self, tmp_path):
        """خروجی JSON درست در فایل ذخیره می‌شه."""
        save_file = tmp_path / "result.json"
        open_ports = [{"port": 443, "service": "https"}]
        with patch("port_scanner.cli.console"):
            output_json("host", "1.1.1.1", open_ports, 1, 1024, 1.5, str(save_file))
        assert save_file.exists()
        data = json.loads(save_file.read_text(encoding="utf-8"))
        assert data["open_ports"][0]["port"] == 443

    def test_empty_ports_json(self, capsys):
        """وقتی پورت بازی نیست، JSON درست تولید می‌شه."""
        output_json("host", "1.1.1.1", [], 1, 1024, 0.5, None)
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert data["open_ports_count"] == 0
        assert data["open_ports"] == []


class TestMain:
    def test_invalid_port_range_exits(self):
        """محدوده پورت نامعتبر باعث exit می‌شه."""
        with patch("sys.argv", ["port-scanner", "host", "-s", "500", "-e", "100"]):
            with patch("port_scanner.cli.console"):
                with pytest.raises(SystemExit):
                    from port_scanner.cli import main
                    main()

    def test_save_without_json_exits(self):
        """استفاده از --save بدون --output json باعث exit می‌شه."""
        with patch("sys.argv", ["port-scanner", "host", "--save", "out.json"]):
            with patch("port_scanner.cli.console"):
                with pytest.raises(SystemExit):
                    from port_scanner.cli import main
                    main()
