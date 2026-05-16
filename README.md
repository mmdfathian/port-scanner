# 🔍 Port Scanner

![CI](https://github.com/mmdfathian/port-scanner/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

---

## ✨ ویژگی‌ها

- اسکن موازی با ThreadPoolExecutor (بسیار سریع)
- خروجی رنگی و زیبا با کتابخانه `rich`
- نمایش spinner انیمیشن حین اسکن
- نمایش نام سرویس هر پورت (http، ssh، ftp و ...)
- پشتیبانی از دامنه و IP
- گزارش جدولی با زمان اجرا
- خروجی JSON برای استفاده در ابزارهای دیگر
- ذخیره گزارش در فایل
- رابط command line کامل

---

## 📦 نصب

```bash
git clone https://github.com/mmdfathian/port-scanner.git
cd port-scanner
pip install -e .
```

---

## 🚀 استفاده

```bash
# اسکن پیش‌فرض (پورت ۱ تا ۱۰۲۴)
port-scanner google.com

# محدوده سفارشی
port-scanner 192.168.1.1 -s 1 -e 500

# با timeout و thread سفارشی
port-scanner example.com -s 1 -e 65535 -t 0.5 -w 200

# خروجی JSON
port-scanner google.com --output json

# ذخیره خروجی JSON در فایل
port-scanner google.com --output json --save result.json
```

### آرگومان‌ها

| آرگومان | پیش‌فرض | توضیح |
|--------|---------|-------|
| `host` | - | آدرس IP یا دامنه هدف |
| `-s, --start` | 1 | شروع محدوده پورت |
| `-e, --end` | 1024 | پایان محدوده پورت |
| `-t, --timeout` | 1.0 | timeout هر اتصال (ثانیه) |
| `-w, --workers` | 100 | تعداد thread های موازی |
| `-o, --output` | text | فرمت خروجی: `text` یا `json` |
| `--save` | - | ذخیره خروجی JSON در فایل |

### نمونه خروجی JSON

```json
{
  "host": "google.com",
  "ip": "142.250.185.46",
  "range": { "start": 1, "end": 1024 },
  "duration_seconds": 3.21,
  "open_ports_count": 2,
  "open_ports": [
    { "port": 80, "service": "http" },
    { "port": 443, "service": "https" }
  ]
}
```

---

## 🧪 اجرای تست‌ها

```bash
pip install -e ".[dev]"
pytest
```

---

## 🗂️ ساختار پروژه

```
port-scanner/
├── port_scanner/
│   ├── __init__.py
│   ├── scanner.py       # منطق اسکن پورت
│   ├── resolver.py      # تبدیل دامنه به IP
│   ├── reporter.py      # نمایش رنگی گزارش با rich
│   └── cli.py           # رابط command line
├── tests/
│   ├── test_scanner.py
│   └── test_resolver.py
├── .github/workflows/
│   ├── ci.yml           # اجرای خودکار تست
│   └── publish.yml      # انتشار روی PyPI
└── pyproject.toml
```

---

## ⚠️ هشدار قانونی

این ابزار را **فقط روی سیستم‌هایی که مجاز به اسکن آن‌ها هستید** استفاده کنید.
اسکن غیرمجاز شبکه‌های دیگران ممکن است غیرقانونی باشد.

---

## 📄 لایسنس

MIT License
