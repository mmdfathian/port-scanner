import socket
import concurrent.futures


def scan_port(host: str, port: int, timeout: float = 1.0) -> tuple[int, bool, str]:
    """ÛŒÚ© Ù¾ÙˆØ±Øª Ø±Ø§ Ø§Ø³Ú©Ù† Ù…ÛŒâ€ŒÚ©Ù†Ø¯."""
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
    Ù¾ÙˆØ±Øªâ€ŒÙ‡Ø§ÛŒ ÛŒÚ© Ù‡Ø§Ø³Øª Ø±Ø§ Ø§Ø³Ú©Ù† Ù…ÛŒâ€ŒÚ©Ù†Ø¯.

    Args:
        host: Ø¢Ø¯Ø±Ø³ IP (Ø§Ø² Ù‚Ø¨Ù„ resolve Ø´Ø¯Ù‡)
        start_port: Ø´Ø±ÙˆØ¹ Ù…Ø­Ø¯ÙˆØ¯Ù‡ Ù¾ÙˆØ±Øª
        end_port: Ù¾Ø§ÛŒØ§Ù† Ù…Ø­Ø¯ÙˆØ¯Ù‡ Ù¾ÙˆØ±Øª
        timeout: timeout Ø¨Ø±Ø§ÛŒ Ù‡Ø± Ø§ØªØµØ§Ù„ (Ø«Ø§Ù†ÛŒÙ‡)
        max_workers: ØªØ¹Ø¯Ø§Ø¯ thread Ù‡Ø§ÛŒ Ù…ÙˆØ§Ø²ÛŒ

    Returns:
        Ù„ÛŒØ³Øª Ù¾ÙˆØ±Øªâ€ŒÙ‡Ø§ÛŒ Ø¨Ø§Ø² Ø¨Ù‡ ØµÙˆØ±Øª dict
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
