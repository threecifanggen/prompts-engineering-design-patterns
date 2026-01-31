"""Yahoo News 新闻获取模块。

功能: 从 Yahoo News (https://news.yahoo.com/) 获取最新新闻列表

工作流程:
1. 发送 HTTP 请求到 Yahoo News 首页
2. 解析 HTML 页面提取新闻条目
3. 提取每条新闻的关键信息（标题、链接、作者、时间）
4. 返回结构化的新闻数据列表

输入参数:
- limit: int - 获取的新闻数量，默认 20
- timeout: int - 请求超时时间（秒），默认 10

输出:
- list[dict[str, str]] - 新闻列表，每个字典包含：
  * title: str - 新闻标题
  * url: str - 新闻链接（完整 URL）
  * author: str - 新闻作者/来源
  * date: str - 新闻发布时间

技术要点:
- 使用 requests 库发送 HTTP 请求
- 使用 BeautifulSoup 解析 HTML
- 处理可能的网络异常和解析错误
- 完整的 Python 3.12 类型注释
- 遵循 PEP 规范

异常处理:
- ConnectionError: 网络连接失败
- TimeoutError: 请求超时
- ValueError: HTML 解析失败或数据格式异常
- Exception: 其他未预期的错误

测试用例:
- 正常获取 20 条新闻
- 指定获取数量（如 10 条）
- 网络异常处理
- 超时处理
- HTML 结构变化的容错处理

依赖:
- requests: HTTP 请求库
- beautifulsoup4: HTML 解析库
- lxml: BeautifulSoup 解析器（可选，性能更好）
"""

import requests
from bs4 import BeautifulSoup
from typing import TypedDict
import urllib3

# 禁用 SSL 警告（仅用于开发测试）
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class YahooNewsItem(TypedDict):
    """Yahoo News 新闻条目类型定义。"""
    title: str
    url: str
    author: str
    date: str


def fetch_yahoo_news(
    limit: int = 20,
    timeout: int = 10
) -> list[dict[str, str]]:
    """从 Yahoo News 获取最新新闻列表。
    
    Args:
        limit: 获取的新闻数量，默认 20
        timeout: 请求超时时间（秒），默认 10
        
    Returns:
        新闻列表，每个字典包含：
        - title: 新闻标题
        - url: 新闻链接
        - author: 新闻作者/来源
        - date: 新闻发布时间
        
    Raises:
        ConnectionError: 网络连接失败
        TimeoutError: 请求超时
        ValueError: HTML 解析失败或数据格式异常
        
    Examples:
        >>> news = fetch_yahoo_news(limit=10)
        >>> len(news)
        10
        >>> news[0]['title']
        'Some interesting news title'
    """
    url = "https://news.yahoo.com/"
    
    try:
        # 发送 HTTP 请求，添加完整的浏览器请求头避免被反爬虫拦截
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        
        # 创建 session 以更好地处理连接
        session = requests.Session()
        session.headers.update(headers)
        
        # 禁用代理
        session.trust_env = False
        proxies = {
            'http': None,
            'https': None,
        }
        
        # 发送请求，关闭 SSL 验证（仅用于开发测试）
        response = session.get(url, timeout=timeout, verify=False, proxies=proxies)
        response.raise_for_status()
    except requests.exceptions.ConnectionError as e:
        raise ConnectionError(f"无法连接到 Yahoo News: {e}") from e
    except requests.exceptions.Timeout as e:
        raise TimeoutError(f"请求超时（{timeout}秒）: {e}") from e
    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"请求失败: {e}") from e
    
    try:
        # 解析 HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        news_items: list[dict[str, str]] = []
        
        # Yahoo News 的 HTML 结构：
        # - 新闻条目在 <li class="stream-item"> 标签中
        # - 标题在 <h3 data-test-locator="stream-item-title"> 内的 <a> 标签
        # - 作者/来源在 <span data-test-locator="stream-item-publisher">
        # - 阅读时间在 <span data-test-locator="stream-read-time">
        
        # 查找所有新闻条目
        stream_items = soup.find_all('li', class_='stream-item', limit=limit * 2)  # 获取更多以防过滤后不足
        
        for item in stream_items:
            if len(news_items) >= limit:
                break
            
            try:
                # 提取标题和链接
                title_elem = item.find('h3', attrs={'data-test-locator': 'stream-item-title'})
                if not title_elem:
                    continue
                
                link = title_elem.find('a')
                if not link:
                    continue
                
                title = link.get_text(strip=True)
                href = link.get('href', '')
                
                # 跳过空标题或无效链接
                if not title or not href:
                    continue
                
                # 处理相对链接
                if href.startswith('/'):
                    href = f"https://news.yahoo.com{href}"
                elif not href.startswith('http'):
                    continue
                
                # 确保链接是新闻文章（包含 /news/ 或 /articles/）
                if '/news/' not in href and '/articles/' not in href:
                    continue
                
                # 提取作者/来源
                author_elem = item.find('span', attrs={'data-test-locator': 'stream-item-publisher'})
                author = author_elem.get_text(strip=True) if author_elem else "Yahoo News"
                
                # 提取时间（阅读时间或其他时间信息）
                time_elem = item.find('span', attrs={'data-test-locator': 'stream-read-time'})
                date = time_elem.get_text(strip=True) if time_elem else "recent"
                
                # 构建新闻条目
                news_item: dict[str, str] = {
                    'title': title,
                    'url': href,
                    'author': author,
                    'date': date
                }
                
                news_items.append(news_item)
                
            except (AttributeError, ValueError, IndexError):
                # 单个条目解析失败，跳过并继续处理下一个
                continue
        
        if not news_items:
            raise ValueError("未能解析出任何新闻条目，HTML 结构可能已变化或需要 JavaScript 渲染")
        
        return news_items
        
    except Exception as e:
        if isinstance(e, ValueError):
            raise
        raise ValueError(f"HTML 解析失败: {e}") from e


def main() -> None:
    """主函数，用于测试。"""
    try:
        print("正在获取 Yahoo News 新闻...")
        news = fetch_yahoo_news(limit=10)
        
        print(f"\n成功获取 {len(news)} 条新闻:\n")
        
        for i, item in enumerate(news, 1):
            print(f"{i}. {item['title']}")
            print(f"   URL: {item['url']}")
            print(f"   作者: {item['author']} | 时间: {item['date']}")
            print()
            
    except (ConnectionError, TimeoutError, ValueError) as e:
        print(f"错误: {e}")
    except Exception as e:
        print(f"未预期的错误: {e}")


if __name__ == "__main__":
    main()
