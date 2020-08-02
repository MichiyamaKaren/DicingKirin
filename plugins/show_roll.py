from nonebot import on_command, CommandSession
from nonebot import permission as perm
from .GroupInfo import Group, load_group, UserFileNotExistError

__plugin_name__ = 'showroll'
__plugin_usage__ = '''显示掷骰结果'''


@on_command('showroll', only_to_me=False)
async def show_roll(session: CommandSession):
    if not await perm.check_permission(session.bot, session.ctx, perm.GROUP):
        session.finish('只能在群聊中使用！')

    player = load_group(session.ctx['group_id']).get_player_from_sender(session.ctx['sender'])
    try:
        await session.send(
            '\n'.join(['{}：{}'.format(
                success,
                '，'.join(['{}{:d}次'.format(skill, n) for skill, n in suc_state.items()]
                         )) for success, suc_state in player.roll_history.items()])
        )
    except UserFileNotExistError:
        session.finish('你并未掷过骰')
