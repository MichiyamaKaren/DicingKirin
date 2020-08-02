import re
from nonebot import on_command, CommandSession
from nonebot import permission as perm
from .GroupInfo import Group, load_group


@on_command('setKP', only_to_me=False)
async def setKP(session: CommandSession):
    group = load_group(session.ctx['group_id'])
    group.KP = session.state['KP']
    await session.send('成功设置KP为[CQ:at,qq={:d}]'.format(session.state['KP']))


@setKP.args_parser
async def _(session: CommandSession):
    if await perm.check_permission(session.bot, session.ctx, perm.SUPERUSER | perm.GROUP_ADMIN):
        arg = session.current_arg_text.strip()
        if arg:
            try:
                session.state['KP'] = int(arg)
            except ValueError:
                session.finish('必须为QQ号或@')
        else:
            try:
                KP, = re.search('\[CQ:at,qq=([0-9]*)\]', session.current_arg).groups()
                session.state['KP'] = int(KP)
            except:
                session.finish('必须为QQ号或@')
    else:
        session.finish('只能由群管理或超级用户设置')