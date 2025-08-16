from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api import logger  # 使用 astrbot 提供的 logger 接口

@register("astrbot_plugin_lqbzgaga", "author", "一个清理缓存的插件", "1.0.0", "repo url")
class CacheCleanerPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    @filter.command("清理群聊缓存")
    async def clean_group_cache(self, event: AstrMessageEvent):
        '''清理群聊缓存指令，格式: /清理群聊缓存 [数字]'''
        # 获取指令后的参数部分
        command_args = event.message_str.split()[1:] if len(event.message_str.split()) > 1 else []
        
        logger.info("触发清理群聊缓存指令!")
        
        # 检查是否有参数且参数是否为数字
        if command_args and command_args[0].isdigit():
            yield event.plain_result("提交成功！立即清理数据！")
        else:
            yield event.plain_result("提交数据错误！")

    @filter.command("清理账号缓存")
    async def clean_account_cache(self, event: AstrMessageEvent):
        '''清理账号缓存指令，格式: /清理账号缓存 [数字]'''
        # 获取指令后的参数部分
        command_args = event.message_str.split()[1:] if len(event.message_str.split()) > 1 else []
        
        logger.info("触发清理账号缓存指令!")
        
        # 检查是否有参数且参数是否为数字
        if command_args and command_args[0].isdigit():
            yield event.plain_result("提交成功！立即清理数据！")
        else:
            yield event.plain_result("提交数据错误！")

    async def terminate(self):
        '''插件被卸载/停用时调用'''
        logger.info("缓存清理插件已停用")
    
