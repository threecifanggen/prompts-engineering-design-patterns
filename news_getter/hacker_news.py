"""Hacker News 新闻获取模块。

功能: 从 Hacker News (https://news.ycombinator.com/) 获取最新新闻列表

工作流程:
1. 发送 HTTP 请求到 Hacker News 首页
2. 解析 HTML 页面提取新闻条目
3. 提取每条新闻的关键信息（标题、链接、得分、作者、时间）
4. 按赞数（score）对新闻进行倒序排列，得分最高的排在前面
5. 返回结构化的新闻数据列表

输入参数:
- limit: int - 获取的新闻数量，默认 30（首页显示数量）
- timeout: int - 请求超时时间（秒），默认 10

输出:
- list[dict[str, str | int]] - 新闻列表（按赞数倒序排列），每个字典包含：
  * title: str - 新闻标题
  * url: str - 新闻链接（可能是外部链接或 HN 讨论链接）
  * score: int - 新闻得分（点数）
  * author: str - 发布者用户名
  * date: str - 发布时间（相对时间，如 "2 hours ago"）

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
- 正常获取 30 条新闻
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


class HackerNewsItem(TypedDict):
    """Hacker News 新闻条目类型定义。"""
    title: str
    url: str
    score: int
    author: str
    date: str


def fetch_hacker_news(
    limit: int = 30,
    timeout: int = 10
) -> list[dict[str, str | int]]:
    """从 Hacker News 获取最新新闻列表。
    
    Args:
        limit: 获取的新闻数量，默认 30（首页默认显示数量）
        timeout: 请求超时时间（秒），默认 10
        
    Returns:
        新闻列表（按赞数倒序排列），每个字典包含：
        - title: 新闻标题
        - url: 新闻链接
        - score: 新闻得分
        - author: 发布者用户名
        - date: 发布时间
        
    Raises:
        ConnectionError: 网络连接失败
        TimeoutError: 请求超时
        ValueError: HTML 解析失败或数据格式异常
        
    Examples:
        >>> news = fetch_hacker_news(limit=10)
        >>> len(news)
        10
        >>> news[0]['title']
        'Some interesting news title'
    """
    url = "https://news.ycombinator.com/"
    
    try:
        # 发送 HTTP 请求
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
    except requests.exceptions.ConnectionError as e:
        raise ConnectionError(f"无法连接到 Hacker News: {e}") from e
    except requests.exceptions.Timeout as e:
        raise TimeoutError(f"请求超时（{timeout}秒）: {e}") from e
    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"请求失败: {e}") from e
    
    try:
        # 解析 HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 查找所有新闻条目
        # Hacker News 的 HTML 结构：
        # - 新闻标题在 <span class="titleline"> 内的 <a> 标签
        # - 元数据（分数、作者、时间）在 <span class="subtext"> 内
        news_items: list[dict[str, str | int]] = []
        
        # 获取所有新闻行（athing class）
        story_rows = soup.find_all('tr', class_='athing', limit=limit)
        
        for story in story_rows:
            try:
                # 提取标题和链接
                titleline = story.find('span', class_='titleline')
                if not titleline:
                    continue
                
                link = titleline.find('a')
                if not link:
                    continue
                
                title = link.get_text(strip=True)
                href = link.get('href', '')
                
                # 处理相对链接（HN 内部链接）
                if href.startswith('item?id='):
                    href = f"https://news.ycombinator.com/{href}"
                
                # 获取元数据行（紧跟在新闻行后面）
                subtext_row = story.find_next_sibling('tr')
                if not subtext_row:
                    continue
                
                subtext = subtext_row.find('td', class_='subtext')
                if not subtext:
                    continue
                
                # 提取得分
                score_span = subtext.find('span', class_='score')
                score = 0
                if score_span:
                    score_text = score_span.get_text(strip=True)
                    # 格式: "123 points"
                    score = int(score_text.split()[0]) if score_text else 0
                
                # 提取作者
                author_link = subtext.find('a', class_='hnuser')
                author = author_link.get_text(strip=True) if author_link else "unknown"
                
                # 提取时间
                age_span = subtext.find('span', class_='age')
                date = "unknown"
                if age_span:
                    age_link = age_span.find('a')
                    date = age_link.get_text(strip=True) if age_link else "unknown"
                
                # 构建新闻条目
                news_item: dict[str, str | int] = {
                    'title': title,
                    'url': href,
                    'score': score,
                    'author': author,
                    'date': date
                }
                
                news_items.append(news_item)
                
            except (AttributeError, ValueError, IndexError) as e:
                # 单个条目解析失败，跳过并继续处理下一个
                continue
        
        if not news_items:
            raise ValueError("未能解析出任何新闻条目，HTML 结构可能已变化")
        
        # 按赞数（score）倒序排列
        news_items.sort(key=lambda x: x['score'], reverse=True)
        
        return news_items
        
    except Exception as e:
        if isinstance(e, ValueError):
            raise
        raise ValueError(f"HTML 解析失败: {e}") from e


def main() -> None:
    """主函数，用于测试。"""
    try:
        print("正在获取 Hacker News 新闻...")
        news = fetch_hacker_news(limit=10)
        
        print(f"\n成功获取 {len(news)} 条新闻:\n")
        
        for i, item in enumerate(news, 1):
            print(f"{i}. {item['title']}")
            print(f"   URL: {item['url']}")
            print(f"   得分: {item['score']} | 作者: {item['author']} | 时间: {item['date']}")
            print()
            
    except (ConnectionError, TimeoutError, ValueError) as e:
        print(f"错误: {e}")
    except Exception as e:
        print(f"未预期的错误: {e}")


if __name__ == "__main__":
    main()
