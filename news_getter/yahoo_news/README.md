# Yahoo News 新闻获取器

从 Yahoo News (https://news.yahoo.com/) 获取最新新闻列表的 Python 模块。

## 功能特性

- ✅ 获取 Yahoo News 首页的最新新闻
- ✅ 提取新闻标题、链接、作者和时间信息
- ✅ 完整的类型注释（Python 3.12）
- ✅ 详细的异常处理
- ✅ 符合 PEP 规范

## 安装依赖

```bash
pip install requests beautifulsoup4 lxml
```

## 使用方法

### 基本使用

```python
from news_getter.yahoo_news import fetch_yahoo_news

# 获取最新的 10 条新闻
news = fetch_yahoo_news(limit=10)

for item in news:
    print(f"标题: {item['title']}")
    print(f"链接: {item['url']}")
    print(f"作者: {item['author']}")
    print(f"时间: {item['date']}")
    print()
```

### 自定义参数

```python
# 获取 20 条新闻，超时时间 15 秒
news = fetch_yahoo_news(limit=20, timeout=15)
```

### 异常处理

```python
try:
    news = fetch_yahoo_news(limit=10)
except ConnectionError as e:
    print(f"网络连接失败: {e}")
except TimeoutError as e:
    print(f"请求超时: {e}")
except ValueError as e:
    print(f"解析失败: {e}")
```

## 返回数据格式

每条新闻是一个字典，包含以下字段：

- `title` (str): 新闻标题
- `url` (str): 新闻链接（完整 URL）
- `author` (str): 新闻作者/来源（如 "Associated Press", "Yahoo News" 等）
- `date` (str): 时间信息（如 "2 min read", "3 min read" 等）

## 注意事项

1. **时间字段**: Yahoo News 首页显示的是阅读时间（如 "2 min read"），而非发布时间
2. **SSL 验证**: 代码中禁用了 SSL 验证以解决某些环境的连接问题（仅用于开发测试）
3. **网络依赖**: 需要能够访问 https://news.yahoo.com/
4. **HTML 结构**: 如果 Yahoo News 更改其网页结构，可能需要更新选择器

## 运行测试

```bash
python -m news_getter.yahoo_news.yahoo_news
```

## 技术细节

- Python 版本: 3.12+
- 使用 requests 进行 HTTP 请求
- 使用 BeautifulSoup 解析 HTML
- 完整的 Google 风格文档字符串
- 符合 PEP 8 编码规范

## 参考实现

本模块参考了 `news_getter/hacker_news.py` 的实现模式。
