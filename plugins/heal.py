from nonebot import on_command, CommandSession
from .Expression import Expression, IllegalExpressionError
from .GroupInfo import Group, load_group

__plugin_name__ = 'heal'
__plugin_usage__ = '''回复HP，用法为heal+随机表达式'''


@on_command('heal', only_to_me=False)
async def Heal(session: CommandSession):
    exp = Expression(session.current_arg_text.strip())
    try:
        heal = exp.parse()
    except IllegalExpressionError as e:
        await session.send('表达式非法：' + str(e))
    else:
        player = load_group(session.ctx['group_id']).get_player_from_sender(session.ctx['sender'])
        oldHP = player.HP
        player.heal(heal)
        await session.send('HP={:.0f}+{:.0f}={:.0f}（不超过最大HP{:.0f}）'.format(
            oldHP, heal, player.HP, player.maxHP),
            at_sender=True)
        player.store()
