from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
from astrbot.api.message_components import Plain
import aiohttp
import urllib.parse

@register(
    "astrbot_plugin_query_report",
    "Your Name",
    "查询与举报插件",
    "v1.0",
    "https://your-repo-url"
)
class QueryAndReport(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        # 配置API地址
        self.query_api = "http://boss.dreamscomtetrue.asia/boss/query.php"
        self.report_api = "http://boss.dreamscomtetrue.asia/boss/submit.php"
        # 请求头设置
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AstrBotPlugin/1.0"
        }

    @filter.command("查询")
    async def handle_query(self, event: AstrMessageEvent, *args):
        """查询功能：/查询 <内容>"""
        # 处理输入参数
        if not args:
            yield event.plain_result("⚠️ 请提供查询内容，使用方法: /查询 <需要查询的内容>")
            return
            
        query_content = " ".join(args)
        
        try:
            # 发送异步请求
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    self.query_api,
                    params={"msg": query_content},
                    headers=self.headers,
                    timeout=10
                ) as response:
                    # 检查响应状态
                    if response.status != 200:
                        yield event.plain_result(f"⚠️ 查询失败，状态码：{response.status}")
                        return
                    
                    # 获取原始响应内容
                    response_text = await response.text()
                    yield event.plain_result(response_text)
                    
        except aiohttp.ClientError as e:
            logger.error(f"查询网络错误：{str(e)}")
            yield event.plain_result("⚠️ 网络请求异常，请检查网络连接")
        except Exception as e:
            logger.error(f"查询处理错误：{str(e)}")
            yield event.plain_result("⚠️ 处理查询时发生错误，请稍后再试")

    @filter.command("举报")
    async def handle_report(self, event: AstrMessageEvent, *args):
        """举报功能：/举报 <内容>"""
        # 处理输入参数
        if not args:
            yield event.plain_result("⚠️ 请提供举报内容，使用方法: /举报 <需要举报的内容>")
            return
            
        report_content = " ".join(args)
        
        try:
            # 发送异步请求
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    self.report_api,
                    params={"msg": report_content},
                    headers=self.headers,
                    timeout=10
                ) as response:
                    # 检查响应状态
                    if response.status != 200:
                        yield event.plain_result(f"⚠️ 举报提交失败，状态码：{response.status}")
                        return
                    
                    # 获取原始响应内容
                    response_text = await response.text()
                    yield event.plain_result(response_text)
                    
        except aiohttp.ClientError as e:
            logger.error(f"举报网络错误：{str(e)}")
            yield event.plain_result("⚠️ 网络请求异常，请检查网络连接")
        except Exception as e:
            logger.error(f"举报处理错误：{str(e)}")
            yield event.plain_result("⚠️ 处理举报时发生错误，请稍后再试")

    async def terminate(self):
        """清理资源"""
        pass
    
