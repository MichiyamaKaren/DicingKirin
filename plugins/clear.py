from nonebot import on_command, CommandSession
from nonebot import permission as perm
from .GroupInfo import Group, load_group

__plugin_name__ = 'clear'
__plugin_usage__ = '清除本群存储的玩家资料'


@on_command('clear')
async def clear(session: CommandSession):
    if await perm.check_permission(session.bot, session.ctx, perm.SUPERUSER | perm.GROUP_ADMIN):
        load_group(session.ctx['group_id']).clear()
        await session.send('已清除本群的玩家资料')
    else:
        await session.send('只有群管理员和超级用户有此权限！')
