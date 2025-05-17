
# 网站静态内容爬虫器

## 概览

这个 Python 脚本用于爬取需要 Cookie 认证的静态网页资源，包括子目录和嵌入资源。

## 功能

* 基于 Cookie 的身份验证
* 支持递归或单目录爬取
* 自动下载嵌入资源 (JS/CSS/图片)
* 识别并筛除登录页面
* 支持手动补充路径

---

## 安装和配置

### 1. 安装依赖

需要 Python 3.7+ ，并且安装相关包：

```bash
pip install -r requirements.txt
```

或者直接安装：

```bash
pip install requests beautifulsoup4
```

### 2. 设置配置

编辑 `public/crawler.py`：

```python
BASE_URL = "https://example.com/static/"
DOWNLOAD_DIR = r"你的本地目录"
```

如需设置 Cookie：

```python
cookies = {
    "Name": "your_cookie_here"
}
```

### 3. 运行脚本

```bash
python crawler.py
```
---
输入函数说明

crawl_and_download(start_url, visited=None, recursive=True, check_auth=True)

start_url（字符串）：起始 URL，用于开始爬取。

visited（集合/None）：已访问过的 URL 集合，防止重复爬取。

recursive（布尔值）：是否递归爬取子目录。

check_auth（布尔值）：是否识别并跳过认证/登录页面。
---

---

## 使用示例

```python
# 递归爬取，并识别登录页
crawl_and_download(BASE_URL, recursive=True, check_auth=True)

# 手动补爬路径
for path in EXTRA_PATHS:
    full_url = urljoin(BASE_URL, path)
    crawl_and_download(full_url, check_auth=False)
```

---

## 提示

* 仅上传 `public` 版本到 GitHub，禁止上传含有个人 Cookie 的版本
* 你可以在本地保留 private 版本，但需通过 `.gitignore` 隔离

---

## 授权协议

MIT License