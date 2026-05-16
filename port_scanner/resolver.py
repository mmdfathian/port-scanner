import socket


def resolve_host(host: str) -> str:
    """
    نام دامنه یا هاست را به آدرس IP تبدیل می‌کند.

    Args:
        host: نام دامنه یا IP

    Returns:
        آدرس IP به صورت string

    Raises:
        ValueError: اگر هاست قابل resolve نباشد
    """
    try:
        return socket.gethostbyname(host)
    except socket.gaierror as e:
        raise ValueError(f"نمی‌توان هاست '{host}' را resolve کرد: {e}")
