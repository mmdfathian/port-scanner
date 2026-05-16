import socket
import concurrent.futures


def scan_port(host: str, port: int, timeout: float = 1.0) -> tuple[int, bool, str]:
    """یک پورت را اسکن می‌کند."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            is_open = result == 0
            service = ""
            if is_open:
                try:
                    service = socket.getservbyport(port)
                except OSError:
                    service = "unknown"
            return port, is_open, service
    except socket.error:
        return port, False, ""


def scan(
    host: str,
    start_port: int = 1,
    end_port: int = 1024,
    timeout: float = 1.0,
    max_workers: int = 100,
) -> list[dict]:
    """
    پورت‌های یک هاست را اسکن می‌کند.

    Args:
        host: آدرس IP (از قبل resolve شده)
        start_port: شروع محدوده پورت
        end_port: پایان محدوده پورت
        timeout: timeout برای هر اتصال (ثانیه)
        max_workers: تعداد thread های موازی

    Returns:
        لیست پورت‌های باز به صورت dict
    """
    open_ports = []
    ports = range(start_port, end_port + 1)

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(scan_port, host, port, timeout): port for port in ports}
        for future in concurrent.futures.as_completed(futures):
            port, is_open, service = future.result()
            if is_open:
                open_ports.append({"port": port, "service": service})

    return sorted(open_ports, key=lambda x: x["port"])
