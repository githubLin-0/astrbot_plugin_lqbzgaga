# 注意：所有导入均来自 astrbot.api 路径，而非直接 from star
from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
from astrbot.api.message_components import Plain
import aiohttp

@register(
    "lin2222",  # 插件唯一标识（需与文件夹名一致）
    "你的名字",
    "查询与举报功能插件",
    "v1.0",
    "https://github.com/githubLin-0/astrbot_plugin_lqbzgaga"  # 你的插件仓库地址
)
class QueryAndReportPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        # 接口地址配置
        self.query_url = "http://boss.dreamscomtetrue.asia/boss/query.php"
        self.report_url = "http://boss.dreamscomtetrue.asia/boss/submit.php"
        # 请求头（模拟浏览器，避免被拦截）
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AstrBot/1.0"
        }

    @filter.command("查询")  # 指令：/查询 <内容>
    async def handle_query(self, event: AstrMessageEvent, *args):
        """查询功能：调用查询接口并返回原始内容"""
        # 检查是否有输入内容
        if not args:
            yield event.plain_result("请使用：/查询 <需要查询的内容>")
            return
        
        # 拼接查询内容（支持带空格的输入）
        query_content = " ".join(args)
        
        try:
            # 异步请求接口（使用aiohttp，避免阻塞）
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    self.query_url,
                    params={"msg": query_content},  # GET参数
                    headers=self.headers,
                    timeout=10  # 超时设置
                ) as response:
                    # 处理HTTP状态码
                    if response.status != 200:
                        yield event.plain_result(f"查询失败，状态码：{response.status}")
                        return
                    # 返回接口原始内容
                    result = await response.text()
                    yield event.plain_result(result)
        
        except aiohttp.ClientError as e:
            logger.error(f"查询网络错误：{str(e)}")
            yield event.plain_result("网络异常，查询失败")
        except Exception as e:
            logger.error(f"查询未知错误：{str(e)}")
            yield event.plain_result("处理查询时出错，请重试")

    @filter.command("举报")  # 指令：/举报 <内容>
    async def handle_report(self, event: AstrMessageEvent, *args):
        """举报功能：调用举报接口并返回原始内容"""
        # 检查是否有输入内容
        if not args:
            yield event.plain_result("请使用：/举报 <需要举报的内容>")
            return
        
        # 拼接举报内容（支持带空格的输入）
        report_content = " ".join(args)
        
        try:
            # 异步请求接口
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    self.report_url,
                    params={"msg": report_content},  # GET参数
                    headers=self.headers,
                    timeout=10
                ) as response:
                    if response.status != 200:
                        yield event.plain_result(f"举报失败，状态码：{response.status}")
                        return
                    # 返回接口原始内容
                    result = await response.text()
                    yield event.plain_result(result)
        
        except aiohttp.ClientError as e:
            logger.error(f"举报网络错误：{str(e)}")
            yield event.plain_result("网络异常，举报失败")
        except Exception as e:
            logger.error(f"举报未知错误：{str(e)}")
            yield event.plain_result("处理举报时出错，请重试")

    async def terminate(self):
        """插件卸载时清理资源（空实现即可）"""
        pass
