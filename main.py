from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
from astrbot.api.message_components import Plain
import aiohttp

@register(
    "astrbot_plugin_lqbzgaga",
    "你的名字",
    "查询与举报功能插件",
    "v1.0",
    "https://github.com/githubLin-0/astrbot_plugin_lqbzgaga"
)
class QueryAndReportPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        self.query_url = "http://boss.dreamscomtetrue.asia/boss/query.php"
        self.report_url = "http://boss.dreamscomtetrue.asia/boss/submit.php"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AstrBot/1.0"
        }

    @filter.command("查询")
    async def handle_query(self, event: AstrMessageEvent, *args):
        if not args:
            yield event.plain_result("使用方法：/查询 <需要查询的内容>")
            return
        
        query_content = " ".join(args)
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    self.query_url,
                    params={"msg": query_content},
                    headers=self.headers,
                    timeout=10
                ) as response:
                    if response.status != 200:
                        yield event.plain_result(f"查询失败，状态码：{response.status}")
                        return
                    result = await response.text()
                    yield event.plain_result(result)
        
        except Exception as e:
            logger.error(f"查询错误: {str(e)}")
            yield event.plain_result("查询时发生错误，请稍后再试")

    @filter.command("举报")
    async def handle_report(self, event: AstrMessageEvent, *args):
        if not args:
            yield event.plain_result("使用方法：/举报 <需要举报的内容>")
            return
        
        report_content = " ".join(args)
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    self.report_url,
                    params={"msg": report_content},
                    headers=self.headers,
                    timeout=10
                ) as response:
                    if response.status != 200:
                        yield event.plain_result(f"举报失败，状态码：{response.status}")
                        return
                    result = await response.text()
                    yield event.plain_result(result)
        
        except Exception as e:
            logger.error(f"举报错误: {str(e)}")
            yield event.plain_result("举报时发生错误，请稍后再试")

    async def terminate(self):
        pass
    
