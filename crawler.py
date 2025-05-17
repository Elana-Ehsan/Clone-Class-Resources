import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, unquote
import re
import time

BASE_URL = "Your Target Website URL"  # 目标网站URL
DOWNLOAD_DIR = r"Your Download Directory Local Path(e.g. C:\Users\YourName\Downloads)"  # 下载目录
cookies = {
    # "cookie_name": "cookie_value",
    # "another_cookie_name": "another_cookie_value"
    # 添加你的 Cookie
    # 例如: "session": "abc123"
}
cookie_header = "; ".join(f"{k}={v}" for k, v in cookies.items())
HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Cookie": cookie_header
}
EXTRA_PATHS = [
    "common/setup/docs/logging-in/",
]

# 请求间隔（秒）/ Request delay (seconds)
REQUEST_DELAY = 2

def is_auth_page(content):
    """检查是否是认证页面 / Check if it is an authentication page"""
    auth_indicators = [
        "CalNet Authentication Service",
        "CalNet ID",
        "Passphrase",
        "Sign In",
        "Forgot CalNet ID or Passphrase"
    ]
    return any(indicator in content for indicator in auth_indicators)

def is_valid_url(url):
    # 排除外部链接（只要不是 http/https 开头，或者是 BASE_URL 开头，都允许）
    # Exclude external links (allow only those not starting with http/https, or starting with BASE_URL)
    if url.startswith('http') and not url.startswith(BASE_URL):
        return False
    # 排除认证相关链接 / Exclude authentication-related links
    if any(x in url.lower() for x in ['auth']):  # 可以添加更多关键词过滤 / Add more keywords if needed
        return False
    return True

def sanitize_filename(filename):
    # 移除或替换 Windows 不允许的字符 / Remove or replace invalid Windows filename characters
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

def ensure_dir(path):
    # 确保目录存在 / Ensure directory exists
    if not os.path.exists(path):
        os.makedirs(path)

def save_html_page(content, full_url):
    # 保存HTML页面 / Save HTML page
    rel_path = full_url.replace(BASE_URL, "")
    rel_path = unquote(rel_path)
    if not rel_path.endswith('/'):
        rel_path += '/'
    rel_path = rel_path.lstrip('/')
    local_dir = os.path.join(DOWNLOAD_DIR, rel_path)
    ensure_dir(local_dir)
    file_path = os.path.join(local_dir, "index.html")  # 保存为 index.html / Save as index.html
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"[保存] 目录页面为: {file_path} / [Saved] Directory page: {file_path}")

def download_file(url, base_url=BASE_URL, check_auth=True):
    # 下载文件 / Download file
    clean_url = url.split('?')[0]
    rel_path = clean_url.replace(base_url, "")
    rel_path = unquote(rel_path)
    rel_path = rel_path.lstrip('/')
    local_path = os.path.join(DOWNLOAD_DIR, rel_path)

    if os.path.exists(local_path):
        print(f"[已存在] {local_path} / [Exists] {local_path}")
        return
    try:
        time.sleep(REQUEST_DELAY)
        print(f"[下载] 开始下载: {url} / [Download] Start: {url}")
        r = requests.get(url, headers=HEADERS)
        print(f"[响应] 状态码: {r.status_code} / [Response] Status code: {r.status_code}")
        if r.status_code == 200:
            if check_auth and is_auth_page(r.text):
                print(f"[跳过] 认证页面 {rel_path} / [Skip] Auth page {rel_path}")
                return
            content_type = r.headers.get('content-type', '')
            # 如果是 HTML 且没有 .html 后缀，自动加上
            # If HTML and no .html suffix, add it automatically
            if content_type.startswith('text/html'):
                if local_path.endswith('/'):
                    local_path = os.path.join(local_path, "index.html")
                elif os.path.isdir(local_path):
                    local_path = os.path.join(local_path, "index.html")
                elif not local_path.endswith('.html'):
                    local_path += ".html"
                print(f"[信息] HTML 文件保存为: {local_path} / [Info] HTML file saved as: {local_path}")


            ensure_dir(os.path.dirname(local_path))
            with open(local_path, 'wb') as f:
                f.write(r.content)
            print(f"[成功] 已下载: {local_path} / [Success] Downloaded: {local_path}")
        else:
            print(f"[失败] 状态码 {r.status_code} - {url} / [Failed] Status code {r.status_code} - {url}")
            print(f"[响应头] {r.headers} / [Response headers] {r.headers}")
    except Exception as e:
        print(f"[异常] {url} -> {e} / [Exception] {url} -> {e}")

def crawl_and_download(start_url, visited=None, recursive=True, check_auth=True):
    # 递归抓取并下载 / Recursively crawl and download
    if visited is None:
        visited = set()

    try:
        clean_url = start_url.split('?')[0]
        if clean_url in visited:
            return
        visited.add(clean_url)

        time.sleep(REQUEST_DELAY)
        print(f"\n[进入目录] {clean_url} / [Enter directory] {clean_url}")
        res = requests.get(clean_url, headers=HEADERS)
        print(f"[响应] 状态码: {res.status_code} / [Response] Status code: {res.status_code}")
        if res.status_code != 200:
            print(f"[跳过] 访问失败 {clean_url} 状态码: {res.status_code} / [Skip] Access failed {clean_url} Status code: {res.status_code}")
            print(f"[响应头] {res.headers} / [Response headers] {res.headers}")
            return

        with open("last_page.html", "w", encoding="utf-8") as f:
            f.write(res.text)

        if check_auth and is_auth_page(res.text):
            print(f"[跳过] 认证页面 {clean_url} / [Skip] Auth page {clean_url}")
            return

        soup = BeautifulSoup(res.text, 'html.parser')
        links = soup.find_all('a')
        print(f"[发现] 本目录下共有 {len(links)} 个链接 / [Found] {len(links)} links in this directory")
        
        save_html_page(res.text, clean_url)

        extra_resources = []
        for tag in soup.find_all(["script", "link", "img"]):
            src = tag.get("src") or tag.get("href")
            if src:
                full_res_url = urljoin(clean_url, src)
                if is_valid_url(full_res_url):
                    extra_resources.append(full_res_url)

        for res_url in extra_resources:
            print(f"[嵌入资源] 发现: {res_url} / [Embedded resource] Found: {res_url}")
            download_file(res_url, check_auth=check_auth)
        
        for a_tag in soup.find_all('a'):
            href = a_tag.get('href')
            text = a_tag.get_text().strip().lower()

            # ==== 过滤无效链接 / Filter invalid links ====
            if not href or href.startswith('#'):
                continue
            if 'parent directory' in text:
                continue
            if '?C=' in href or ';O=' in href:
                continue
            if not is_valid_url(href):
                continue

            full_url = urljoin(clean_url, href)
            print(f"[处理] 链接: {full_url} / [Process] Link: {full_url}")

            # 如果是目录，递归进入 / If directory, recurse
            if full_url.endswith('/'):
                if recursive:
                    crawl_and_download(full_url, visited, recursive)
                else:
                    print(f"[跳过子目录] {full_url} / [Skip subdirectory] {full_url}")
            # 如果是文件，直接下载 / If file, download directly
            else:
                print(f"[准备下载] 文件: {full_url} / [Prepare to download] File: {full_url}")
                download_file(full_url, check_auth=check_auth)
                print(f"[完成下载] 文件: {full_url} / [Finished download] File: {full_url}")

    except Exception as e:
        print(f"[抓取失败] {start_url}: {e} / [Crawl failed] {start_url}: {e}")

# 运行 / Run
#crawl_and_download(BASE_URL,recursive=True,check_auth=True)#1 Basic Use
#2 Some Extra Paths that are not catched
""" for path in EXTRA_PATHS:
    full_url = urljoin(BASE_URL, path)
    print(f"[手动补抓] {full_url} / [Manual extra crawl] {full_url}")
    crawl_and_download(full_url,check_auth=False) """
#3 No Auth Use
crawl_and_download(BASE_URL, recursive=False, check_auth=False)