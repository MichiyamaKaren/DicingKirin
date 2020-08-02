from nonebot import on_command, CommandSession
from .GroupInfo import Group, load_group

__plugin_name__ = 'KPstate'
__plugin_usage__ = '''KP通过这一命令可以设置自己为NPC，可以像玩家一样存储技能和掷骰'''


@on_command('KPstate', aliases=('kpstate',), only_to_me=False)
async def KPstate(session: CommandSession):
    group = load_group(session.state['group_id'])
    if session.ctx['user_id'] != group.KP:
        session.finish('只能KP设置！')
    group.KP_state = session.current_arg_text.strip()
    group.store()
    await session.send('KP_state成功设置为' + group.KP_state)
