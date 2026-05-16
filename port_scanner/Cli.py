import argparse
from datetime import datetime

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from port_scanner.resolver import resolve_host
from port_scanner.scanner import scan
from port_scanner.reporter import print_report

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
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.start < 1 or args.end > 65535 or args.start > args.end:
        console.print("[bold red]خطا:[/bold red] محدوده پورت نامعتبر است. (1 تا 65535)")
        return

    console.print(f"\n[bold cyan]شروع اسکن:[/bold cyan] [white]{args.host}[/white]")
    console.print(
        f"[bold cyan]زمان شروع:[/bold cyan] "
        f"[white]{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}[/white]\n"
    )

    try:
        ip = resolve_host(args.host)
        start_time = datetime.now()

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

        duration = (datetime.now() - start_time).total_seconds()
        print_report(args.host, ip, open_ports, args.start, args.end, duration)

    except ValueError as e:
        console.print(f"[bold red]خطا:[/bold red] {e}")


if __name__ == "__main__":
    main()
