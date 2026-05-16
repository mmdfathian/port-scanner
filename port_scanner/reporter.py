def print_report(
    host: str,
    ip: str,
    open_ports: list[dict],
    start_port: int,
    end_port: int,
    duration: float,
) -> None:
    """
    گزارش نتایج اسکن را چاپ می‌کند.

    Args:
        host: نام هاست یا IP اصلی
        ip: آدرس IP resolve شده
        open_ports: لیست پورت‌های باز
        start_port: شروع محدوده اسکن
        end_port: پایان محدوده اسکن
        duration: مدت زمان اسکن به ثانیه
    """
    print("\n" + "=" * 50)
    print("  گزارش اسکن پورت")
    print("=" * 50)
    print(f"  هدف    : {host} ({ip})")
    print(f"  محدوده : {start_port} - {end_port}")
    print(f"  زمان   : {duration:.2f} ثانیه")
    print("=" * 50)

    if open_ports:
        print(f"\n  پورت‌های باز ({len(open_ports)} عدد):\n")
        print(f"  {'پورت':<10} {'سرویس'}")
        print(f"  {'-' * 10} {'-' * 15}")
        for entry in open_ports:
            print(f"  {entry['port']:<10} {entry['service']}")
    else:
        print("\n  هیچ پورت بازی یافت نشد.")

    print("\n" + "=" * 50)
