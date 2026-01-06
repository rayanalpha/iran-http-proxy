# Iranian Proxy Checker (Health System Specialized)
---

## 🇺🇸 English Guide

This tool is designed to fetch and validate Iranian HTTP proxies specifically for accessing geo-restricted services such as the Iranian National Health System (`salamat.gov.ir`).

### 🚀 Key Features
- **High Performance:** Utilizes Python's `concurrent.futures` with 50 concurrent threads for rapid validation.
- **Two-Stage Verification:** 
    1. **Connectivity Check:** Verifies general internet access via Google.
    2. **Target Validation:** Confirms specific access to the Health System portal.
- **Automated Data Aggregation:** Fetches live proxy lists from multiple reliable APIs.
- **Output Management:** Automatically saves validated proxies to `working_proxies.txt` for further use.

### 🛠 Installation & Usage
1. **Prerequisites:** Ensure the `requests` library is installed:
   ```bash
   pip install requests
   ```
2. **Execution:** Run the script using Python:
   ```bash
   python3 proxy_checker.py
   ```
3. **Results:** Monitor the terminal for real-time status and check the generated text file for the final list.

---

## 🇮🇷 راهنمای فارسی

این ابزار برای دریافت و اعتبارسنجی پروکسی‌های HTTP ایران به منظور دسترسی به سرویس‌های دارای محدودیت جغرافیایی، از جمله سامانه سلامت (`salamat.gov.ir`) طراحی شده است.

### 🌟 قابلیت‌های کلیدی
- **عملکرد بهینه:** استفاده از مدل چندرشته‌ای (Multi-threading) با ۵۰ هسته فعال جهت بررسی سریع هزاران پروکسی.
- **تأیید دو مرحله‌ای:** 
    ۱. **بررسی اتصال:** اطمینان از زنده بودن پروکسی از طریق اتصال به سرویس‌های گوگل.
    ۲. **بررسی هدف:** اعتبارسنجی نهایی جهت اطمینان از توانایی باز کردن سامانه سلامت.
- **تأمین خودکار منابع:** دریافت لیست‌های بروز از چندین منبع معتبر بصورت همزمان.
- **مدیریت نتایج:** ذخیره‌سازی خودکار پروکسی‌های تأیید شده در فایل `working_proxies.txt`.

### ⚙️ پیش‌نیازها و نحوه اجرا
۱. **نصب کتابخانه‌ها:** ابتدا کتابخانه `requests` را نصب نمایید:
   ```bash
   pip install requests
   ```
۲. **اجرا:** اسکریپت را از طریق مفسر پایتون اجرا کنید:
   ```bash
   python3 proxy_checker.py
   ```
۳. **خروجی:** پس از اتمام فرآیند، لیست نهایی پروکسی‌های سالم در فایل متنی در کنار اسکریپت قابل مشاهده خواهد بود.

---

**Disclaimer:** This tool is for educational and legitimate testing purposes only.
**سلب مسئولیت:** این ابزار صرفاً جهت مقاصد آموزشی و تست‌های قانونی طراحی شده است.
