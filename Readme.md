# Website Static Content Crawler (Cookie Authenticated)

# 网站静态内容爬虫器

# 🌐 Choose Language | 选择语言

- [中文说明文档](README.zh.md)

## 🚀 Overview

This Python script downloads and mirrors part of a cookie-authenticated static website, including subdirectories and embedded resources.

## 🔧 Features

* Cookie-based authentication
* Recursive or single-directory crawling
* Embedded resources (JS, CSS, images) supported
* Login page detection and skipping
* Manual path supplementation (for pages not listed)

## ⚠️ Disclaimer

**Do not share your cookies.** This repository only contains the public version with no private cookie data. You should maintain your cookie and authentication configurations separately.


## 🔧 Installation & Setup

### 1. Install Dependencies

Ensure you have Python 3.7+ and install required packages:

```bash
pip install -r requirements.txt
```

If you don’t have a `requirements.txt`, install directly:

```bash
pip install requests beautifulsoup4
```

### 2. Set Configuration

Edit `public/crawler.py`:

```python
BASE_URL = "https://example.com/static/"
DOWNLOAD_DIR = r"Your local directory"
```

Insert your cookie manually if needed:

```python
cookies = {
    "Name": "your_cookie_here"
}
```

### 3. Run Script

```bash
python crawler.py
```

---
🧠 Input Function Description

crawl_and_download(start_url, visited=None, recursive=True, check_auth=True)

start_url (str): The starting URL to begin crawling from.

visited (set or None): A set of already-visited URLs to avoid reprocessing. Default is None, which initializes an empty set.

recursive (bool): Whether to recursively crawl subdirectories. Set False to crawl only the current directory.

check_auth (bool): Whether to detect and skip login/authentication pages. Set False if already authenticated or unnecessary.
---


## 🔄 Usage Examples

```python
# Basic recursive crawl with login page detection
crawl_and_download(BASE_URL, recursive=True, check_auth=True)

# Manually crawl specific paths
for path in EXTRA_PATHS:
    full_url = urljoin(BASE_URL, path)
    crawl_and_download(full_url, check_auth=False)
```

---

## 🔗 License

MIT License

---
