from star import Plugin, register, Message, LLM
import requests
from typing import Optional

class ReportQueryPlugin(Plugin):
    """举报与查询插件
    
    提供/查询和/举报两个指令，分别调用指定的API接口
    并返回接口的原始响应内容
    """
    # 插件元数据
    name: str = "举报查询插件"
    description: str = "提供内容查询与举报功能"
    version: str = "1.0.0"
    author: str = "Your Name"
    # 指令前缀，遵循文档规范
    command_prefix: str = "/"

    def __init__(self):
        super().__init__()
        # API接口配置
        self.query_url = "http://boss.dreamscomtetrue.asia/boss/query.php"
        self.report_url = "http://boss.dreamscomtetrue.asia/boss/submit.php"

    @register(
        command="查询",
        help="查询指定内容\n使用方法: /查询 <需要查询的内容>",
        description="调用查询接口获取信息"
    )
    async def handle_query(self, llm: LLM, message: Message) -> Optional[str]:
        """处理/查询指令"""
        # 提取指令参数（去除"/查询"前缀）
        query_content = message.content[len("/查询"):].strip()
        
        if not query_content:
            return "❌ 请提供查询内容，使用方法: /查询 <内容>"
        
        try:
            # 调用API接口
            response = requests.get(
                url=self.query_url,
                params={"msg": query_content},
                timeout=10  # 设置超时时间，避免阻塞
            )
            # 确保请求成功
            response.raise_for_status()
            # 返回原始响应内容
            return response.text
        
        except requests.exceptions.Timeout:
            return "⏰ 查询超时，请稍后再试"
        except requests.exceptions.RequestException as e:
            return f"❌ 查询失败: {str(e)}"
        except Exception as e:
            return f"⚠️ 处理查询时发生错误: {str(e)}"

    @register(
        command="举报",
        help="举报指定内容\n使用方法: /举报 <需要举报的内容>",
        description="提交举报内容到指定接口"
    )
    async def handle_report(self, llm: LLM, message: Message) -> Optional[str]:
        """处理/举报指令"""
        # 提取指令参数（去除"/举报"前缀）
        report_content = message.content[len("/举报"):].strip()
        
        if not report_content:
            return "❌ 请提供举报内容，使用方法: /举报 <内容>"
        
        try:
            # 调用API接口
            response = requests.get(
                url=self.report_url,
                params={"msg": report_content},
                timeout=10  # 设置超时时间，避免阻塞
            )
            # 确保请求成功
            response.raise_for_status()
            # 返回原始响应内容
            return response.text
        
        except requests.exceptions.Timeout:
            return "⏰ 举报提交超时，请稍后再试"
        except requests.exceptions.RequestException as e:
            return f"❌ 举报提交失败: {str(e)}"
        except Exception as e:
            return f"⚠️ 处理举报时发生错误: {str(e)}"

# 实例化插件
plugin = ReportQueryPlugin()
    
