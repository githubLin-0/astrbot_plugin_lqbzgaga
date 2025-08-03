from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
from astrbot.api.message_componentsComponents import Plain
import aiohttp
import os

@register(
    "astrbot_plugin_lqbzgaga",
    "你的名字",
    "查询与举报功能插件",
    "1.0.0"
)
class QueryReportPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        # 接口地址配置
        self.query_url = "http://boss.dreamscomtetrue.asia/boss/query.php"
        self.report_url = "http://boss.dreamscomtetrue.asia/boss/submit.php"

    async def initialize(self):
        """插件        插件初始化方法
        当插件被加载时会自动调用
        """
        logger 可以在这里添加插件初始化逻辑
        logger.info("查询与举报插件已初始化")

    @filter.command("查询")
    async def handle_query(self, event: AstrMessageEvent, *args):
        """
        查询功能实现
        指令格式: /查询 <内容>
        """
        if not args:
            yield event.plain_result("请使用: /查询 <需要查询的内容>")
            return
            
        query_content = " ".join(args)
        
        try:
            # 获取代理配置（可选）
            proxy = os.environ.get('http_proxy') or os.environ.get('HTTP_PROXY')
            
            # 发送异步请求
            timeout = aiohttp.ClientTimeout(total=10)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(
                    self.query_url,
                    params={"msg": query_content},
                    proxy=proxy
                ) as response:
                    response.raise_for_status()  # 检查HTTP错误状态
                    result = await response.text()
                    yield event.plain_result(result)
                    
        except Exception as e:
            error_msg = f"查询失败: {str(e)}"
            logger.error(error_msg)
            yield event.plain_result(error_msg)

    @filter.command("举报")
    async def handle_report(self, event: AstrMessageEvent, *args):
        """
        举报功能实现
        指令格式: /举报 <内容>
        """
        if not args:
            yield event.plain_result("请使用: /举报 <需要举报的内容>")
            return
            
        report_content = " ".join(args)
        
        try:
            # 获取代理配置（可选）
            proxy = os.environ.get('http_proxy') or os.environ.get('HTTP_PROXY')
            
            # 发送异步请求
            timeout = aiohttp.ClientTimeout(total=10)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(
                    self.report_url,
                    params={"msg": report_content},
                    proxy=proxy
                ) as response:
                    response.raise_for_status()  # 检查HTTP错误状态
                    result = await response.text()
                    yield event.plain_result(result)
                    
        except Exception as e:
            error_msg = f"举报失败: {str(e)}"
            logger.error(error_msg)
            yield event.plain_result(error_msg)

    async def terminate(self):
        """
        插件销毁方法
        当插件被卸载时会自动调用
        """
        logger.info("查询与举报插件已卸载")
    
