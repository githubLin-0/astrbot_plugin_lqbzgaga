from star import LLM, Plugin, register, Message, EventType
import requests

class ReportAndQueryPlugin(Plugin):
    name = "举报与查询插件"
    description = "提供/举报和/查询功能，对接指定API接口"
    version = "1.0.0"
    author = "Your Name"

    def __init__(self):
        super().__init__()
        # 配置API地址
        self.query_api = "http://boss.dreamscomtetrue.asia/boss/query.php"
        self.report_api = "http://boss.dreamscomtetrue.asia/boss/submit.php"

    @register(command="/查询", help="使用方法: /查询 <内容> - 查询指定内容")
    async def handle_query(self, llm: LLM, message: Message):
        # 提取查询内容
        query_content = message.content.strip()[3:].strip()  # 去除"/查询"前缀
        
        if not query_content:
            return "请提供要查询的内容，使用方法: /查询 <内容>"
        
        try:
            # 调用查询API
            response = requests.get(f"{self.query_api}?msg={query_content}")
            # 返回原始响应内容
            return response.text
        except Exception as e:
            return f"查询失败: {str(e)}"

    @register(command="/举报", help="使用方法: /举报 <内容> - 举报指定内容")
    async def handle_report(self, llm: LLM, message: Message):
        # 提取举报内容
        report_content = message.content.strip()[3:].strip()  # 去除"/举报"前缀
        
        if not report_content:
            return "请提供要举报的内容，使用方法: /举报 <内容>"
        
        try:
            # 调用举报API
            response = requests.get(f"{self.report_api}?msg={report_content}")
            # 返回原始响应内容
            return response.text
        except Exception as e:
            return f"举报提交失败: {str(e)}"

# 插件入口
plugin = ReportAndQueryPlugin()
