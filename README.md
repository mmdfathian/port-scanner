# 🔍 Port Scanner

![CI](https://github.com/mmdfathian/port-scanner/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

---

## ✨ ویژگی‌ها

- اسکن موازی با ThreadPoolExecutor (بسیار سریع)
- نمایش نام سرویس هر پورت (http، ssh، ftp و ...)
- پشتیبانی از دامنه و IP
- گزارش مرتب با زمان اجرا
- رابط command line کامل

---

## 📦 نصب

```bash
git clone https://github.com/YOUR_USERNAME/port-scanner.git
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
```

### آرگومان‌ها

| آرگومان | پیش‌فرض | توضیح |
|--------|---------|-------|
| `host` | - | آدرس IP یا دامنه هدف |
| `-s, --start` | 1 | شروع محدوده پورت |
| `-e, --end` | 1024 | پایان محدوده پورت |
| `-t, --timeout` | 1.0 | timeout هر اتصال (ثانیه) |
| `-w, --workers` | 100 | تعداد thread های موازی |

---

## 🧪 اجرای تست‌ها

```bash
pip install -e ".[dev]"
pytest
```

---

## ⚠️ هشدار قانونی

این ابزار را **فقط روی سیستم‌هایی که مجاز به اسکن آن‌ها هستید** استفاده کنید.
اسکن غیرمجاز شبکه‌های دیگران ممکن است غیرقانونی باشد.

---

## 📄 لایسنس

MIT License
