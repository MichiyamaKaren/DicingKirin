from nonebot import on_command, CommandSession
from nonebot import permission as perm
from .GroupInfo import Group, load_group, UserFileNotExistError

__plugin_name__ = 'storeroll(stroll)'
__plugin_usage__ = '''手动存储掷骰结果，用法为：
stroll 掷骰结果 技能 [次数]
结果只能为：大失败、失败、成功、困难成功、极困难成功、大成功 之一
次数不提供默认为一次'''


@on_command('storeroll', aliases=('stroll',), only_to_me=False)
async def store_roll(session: CommandSession):
    player = load_group(session.ctx['group_id']).get_player_from_sender(session.ctx['sender'])
    player.store_roll(session.state['skill'], 0, session.state['success'], session.state['n'])
    await session.send('成功存储掷骰结果')


@store_roll.args_parser
async def _(session: CommandSession):
    if not await perm.check_permission(session.bot, session.ctx, perm.GROUP):
        session.finish('只能在群聊中使用！')

    try:
        args = session.current_arg_text.split()
        success, skill = args[:2]
        n = 1
        if len(args) == 3:
            n = int(args[2])
        if success not in ['大失败', '失败', '成功', '困难成功', '极困难成功', '大成功']:
            raise Exception

        session.state['success'] = success
        session.state['skill'] = skill
        session.state['n'] = n

    except:
        session.finish('格式错误，使用help指令查看调用方法')
