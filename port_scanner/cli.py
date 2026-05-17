import argparse
import json
import sys
from datetime import datetime

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from port_scanner.reporter import print_report
from port_scanner.resolver import resolve_host
from port_scanner.scanner import scan

console = Console()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Port Scanner حرفه‌ای با پایتون",
        epilog="مثال: port-scanner google.com -s 1 -e 1024",
    )
    parser.add_argument("host", help="آدرس IP یا دامنه هدف")
    parser.add_argument("-s", "--start", type=int, default=1, help="شروع پورت (پیش‌فرض: 1)")
    parser.add_argument("-e", "--end", type=int, default=1024, help="پایان پورت (پیش‌فرض: 1024)")
    parser.add_argument(
        "-t", "--timeout", type=float, default=1.0, help="timeout به ثانیه (پیش‌فرض: 1.0)"
    )
    parser.add_argument(
        "-w", "--workers", type=int, default=100, help="تعداد thread (پیش‌فرض: 100)"
    )
    parser.add_argument(
        "-o",
        "--output",
        choices=["text", "json"],
        default="text",
        help="فرمت خروجی (پیش‌فرض: text)",
    )
    parser.add_argument("--save", default=None, help="ذخیره خروجی JSON در فایل")
    return parser


def output_json(
    host: str,
    ip: str,
    open_ports: list[dict],
    start_port: int,
    end_port: int,
    duration: float,
    save_path: str | None,
) -> None:
    """خروجی JSON تولید و چاپ می‌کند."""
    result = {
        "host": host,
        "ip": ip,
        "range": {"start": start_port, "end": end_port},
        "duration_seconds": round(duration, 2),
        "open_ports_count": len(open_ports),
        "open_ports": open_ports,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))

    if save_path:
        with open(save_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        console.print(f"[green]گزارش در فایل ذخیره شد:[/green] {save_path}")


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.start < 1 or args.end > 65535 or args.start > args.end:
        console.print("[bold red]خطا:[/bold red] محدوده پورت نامعتبر است. (1 تا 65535)")
        sys.exit(1)

    if args.save and args.output != "json":
        console.print("[bold red]خطا:[/bold red] --save فقط با --output json قابل استفاده است.")
        sys.exit(1)

    console.print(f"\n[bold cyan]شروع اسکن:[/bold cyan] [white]{args.host}[/white]")
    console.print(
        f"[bold cyan]زمان شروع:[/bold cyan] "
        f"[white]{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}[/white]\n"
    )

    try:
        ip = resolve_host(args.host)
        start_time = datetime.now()

        if args.output == "text":
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                transient=True,
            ) as progress:
                progress.add_task(
                    f"[yellow]در حال اسکن پورت‌های {args.start} تا {args.end}...[/yellow]",
                    total=None,
                )
                open_ports = scan(
                    host=ip,
                    start_port=args.start,
                    end_port=args.end,
                    timeout=args.timeout,
                    max_workers=args.workers,
                )
        else:
            open_ports = scan(
                host=ip,
                start_port=args.start,
                end_port=args.end,
                timeout=args.timeout,
                max_workers=args.workers,
            )

        duration = (datetime.now() - start_time).total_seconds()

        if args.output == "json":
            output_json(args.host, ip, open_ports, args.start, args.end, duration, args.save)
        else:
            print_report(args.host, ip, open_ports, args.start, args.end, duration)

    except ValueError as e:
        console.print(f"[bold red]خطا:[/bold red] {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
