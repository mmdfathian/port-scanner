import argparse
import json
import time
from rich.console import Console
from port_scanner.scanner import scan
from port_scanner.resolver import resolve_host
from port_scanner.reporter import print_report

console = Console()


def build_parser():
    """ساخت parser برای آرگومان‌های command line."""
    parser = argparse.ArgumentParser(
        description="ابزار سریع اسکن پورت‌های شبکه با پشتیبانی اسکن موازی"
    )
    parser.add_argument("host", help="هاست یا نام دامنه برای اسکن")
    parser.add_argument(
        "-s",
        "--start",
        type=int,
        default=1,
        help="شروع محدوده پورت (پیش‌فرض: 1)",
    )
    parser.add_argument(
        "-e",
        "--end",
        type=int,
        default=1024,
        help="پایان محدوده پورت (پیش‌فرض: 1024)",
    )
    parser.add_argument(
        "-t",
        "--timeout",
        type=float,
        default=1.0,
        help="timeout برای هر اتصال به ثانیه (پیش‌فرض: 1.0)",
    )
    parser.add_argument(
        "-w",
        "--workers",
        type=int,
        default=100,
        help="تعداد worker threads (پیش‌فرض: 100)",
    )
    parser.add_argument(
        "--output",
        choices=["text", "json"],
        default="text",
        help="فرمت خروجی (پیش‌فرض: text)",
    )
    parser.add_argument(
        "--save",
        help="ذخیره خروجی در فایل (نیازمند --output json)",
    )
    return parser


def output_json(host, ip, open_ports, start, end, duration_seconds, save_path):
    """خروجی نتایج به فرمت JSON."""
    data = {
        "host": host,
        "ip": ip,
        "range": f"{start}-{end}",
        "duration_seconds": duration_seconds,
        "open_ports_count": len(open_ports),
        "open_ports": open_ports,
    }

    json_output = json.dumps(data, indent=2, ensure_ascii=False)
    console.print(json_output)

    if save_path:
        with open(save_path, "w", encoding="utf-8") as f:
            f.write(json_output)


def main():
    """نقطه ورود اصلی CLI."""
    parser = build_parser()
    args = parser.parse_args()

    # اعتبار‌سنجی محدوده پورت
    if args.start > args.end:
        console.print("[red]خطا: پورت شروع باید کمتر یا مساوی پورت پایان باشد[/red]")
        raise SystemExit(1)

    # اعتبار‌سنجی فلگ --save
    if args.save and args.output != "json":
        console.print("[red]خطا: --save نیازمند --output json است[/red]")
        raise SystemExit(1)

    try:
        # resolve کردن هاست
        console.print(f"[cyan]درحال resolve کردن {args.host}...[/cyan]")
        ip = resolve_host(args.host)
        console.print(f"[green]✓[/green] {args.host} -> {ip}\n")

        # شروع اسکن
        console.print(f"[cyan]درحال اسکن پورت‌های {ip}...[/cyan]")
        start_time = time.time()
        open_ports = scan(ip, args.start, args.end, args.timeout, args.workers)
        duration = time.time() - start_time

        # نمایش نتایج
        if args.output == "json":
            output_json(args.host, ip, open_ports, args.start, args.end, duration, args.save)
        else:
            print_report(args.host, ip, open_ports, args.start, args.end, duration)

    except ValueError as e:
        console.print(f"[red]خطا: {e}[/red]")
        raise SystemExit(1)
    except KeyboardInterrupt:
        console.print("\n[yellow]⚠ اسکن توسط کاربر متوقف شد[/yellow]")
        raise SystemExit(1)
    except Exception as e:
        console.print(f"[red]خطای غیرمنتظره: {e}[/red]")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
