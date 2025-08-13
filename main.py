import os
import json
from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
from astrbot.api.message_components import Plain
import aiohttp
import json

@register("astrbot_plugin_lqbzgaga", "your_name", "学校查询插件", "1.0", "https://github.com/your_repo/school-query")
class SchoolQueryPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
        }
        self.base_url = 'https://api.52vmy.cn/api/query/daxue'

    @filter.command("查学校")
    async def search_school(self, event: AstrMessageEvent):
        '''查询学校信息\n用法：/查学校 学校名称'''
        args = event.message_str.split(maxsplit=1)
        if len(args) < 2:
            yield event.plain_result("请输入要查询的学校名称，例如：/查学校 武汉大学")
            return
        
        school_name = args[1]
        try:
            # 构建请求参数
            params = {
                'daxue': school_name
            }
            
            async with aiohttp.ClientSession(headers=self.headers) as session:
                async with session.get(self.base_url, params=params) as resp:
                    # 确保请求成功
                    if resp.status != 200:
                        yield event.plain_result(f"查询失败，状态码：{resp.status}")
                        return
                    
                    # 解析JSON响应
                    response_data = await resp.json()

            # 检查返回数据是否存在
            if not response_data or 'data' not in response_data:
                yield event.plain_result(f"未找到与「{school_name}」相关的学校信息")
                return
            
            school_info = response_data['data']
            
            # 构建回复消息
            msg = [f"🔍找到「{school_name}」的信息：\n"]
            
            # 提取常见学校信息（根据接口返回字段调整）
            info_mapping = {
                'name': '学校名称',
                'address': '地址',
                'level': '学校层次',
                'type': '学校类型',
                'found_time': '创办时间',
                'description': '学校简介'
            }
            
            for key, label in info_mapping.items():
                if key in school_info and school_info[key]:
                    msg.append(f"   📌 【{label}】：{school_info[key]}")
            
            # 处理可能存在的特色专业信息
            if 'specialties' in school_info and school_info['specialties']:
                specialties = ', '.join(school_info['specialties'])
                msg.append(f"   🌟 【特色专业】：{specialties}")
            
            # 处理其他可能的字段
            if 'website' in school_info and school_info['website']:
                msg.append(f"   🌐 【学校官网】：{school_info['website']}")

            yield event.plain_result("\n".join(msg))

        except json.JSONDecodeError:
            logger.error("解析学校信息失败：响应不是有效的JSON")
            yield event.plain_result("查询到的学校信息格式错误")
        except Exception as e:
            logger.error(f"学校查询失败: {str(e)}", exc_info=True)
            yield event.plain_result("学校查询服务暂时不可用，请稍后再试")

    async def terminate(self):
        '''清理资源'''
        pass
