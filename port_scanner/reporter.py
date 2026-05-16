from rich.console import Console
from rich.table import Table
from rich import box
from rich.panel import Panel
from rich.text import Text

console = Console()


def print_report(
    host: str,
    ip: str,
    open_ports: list[dict],
    start_port: int,
    end_port: int,
    duration: float,
) -> None:
    """
    گزارش رنگی نتایج اسکن را چاپ می‌کند.

    Args:
        host: نام هاست یا IP اصلی
        ip: آدرس IP resolve شده
        open_ports: لیست پورت‌های باز
        start_port: شروع محدوده اسکن
        end_port: پایان محدوده اسکن
        duration: مدت زمان اسکن به ثانیه
    """
    # هدر
    info = Text()
    info.append("هدف    : ", style="bold cyan")
    info.append(f"{host} ({ip})\n", style="white")
    info.append("محدوده : ", style="bold cyan")
    info.append(f"{start_port} - {end_port}\n", style="white")
    info.append("زمان   : ", style="bold cyan")
    info.append(f"{duration:.2f} ثانیه", style="white")

    console.print(Panel(info, title="[bold blue]گزارش اسکن پورت[/bold blue]", expand=False))

    if open_ports:
        table = Table(
            box=box.ROUNDED,
            show_header=True,
            header_style="bold magenta",
            title=f"[green]پورت‌های باز ({len(open_ports)} عدد)[/green]",
        )
        table.add_column("پورت", style="bold green", justify="center", min_width=8)
        table.add_column("سرویس", style="yellow", justify="center", min_width=15)

        for entry in open_ports:
            table.add_row(str(entry["port"]), entry["service"] or "-")

        console.print(table)
    else:
        console.print(
            Panel("[bold red]هیچ پورت بازی یافت نشد.[/bold red]", expand=False)
        )

