# Yahoo News 新闻获取模块

## 功能需求
从 Yahoo News (https://news.yahoo.com/) 获取最新新闻列表

## 工作流程
1. 发送 HTTP 请求到 Yahoo News 首页
2. 使用 BeautifulSoup 解析 HTML 页面
3. 提取新闻条目的关键信息（标题、链接、作者、时间）
4. 返回结构化的新闻数据列表

## 输入参数
- limit: int - 获取的新闻数量，默认 20
- timeout: int - 请求超时时间（秒），默认 10

## 输出格式
- 类型: list[dict[str, str]]
- 每个 dict 包含：
  * title: str - 新闻标题
  * url: str - 新闻链接（完整 URL）
  * author: str - 新闻作者/来源
  * date: str - 新闻发布时间

## 技术要点
- 使用 Python 3.12 类型注解（TypedDict）
- 使用 requests 库进行 HTTP 请求
- 使用 BeautifulSoup 解析 HTML
- 完整的异常处理机制
- 详细的文档字符串（模块级和函数级）
- 遵循 PEP 规范

## 异常处理
- ConnectionError: 网络连接失败
- TimeoutError: 请求超时
- ValueError: HTML 解析失败或数据格式异常
- Exception: 其他未预期的错误

## 测试用例
- 正常获取新闻列表（默认数量）
- 指定获取数量（如 10 条）
- 网络异常处理测试
- 超时处理测试
- HTML 结构变化的容错处理

## 实现参考
参考 `news_getter/hacker_news.py` 的实现模式：
- TypedDict 定义数据结构
- 完整的异常捕获和转换
- 详细的模块文档字符串
- main() 测试函数

## 依赖库
- requests: HTTP 请求
- beautifulsoup4: HTML 解析
- lxml: BeautifulSoup 解析器（可选）