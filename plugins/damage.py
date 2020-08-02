from nonebot import on_command, CommandSession
from .Expression import Expression, IllegalExpressionError
from .GroupInfo import Group, load_group

__plugin_name__ = 'damage'
__plugin_usage__ = '''扣除HP，用法为damage+随机表达式'''


@on_command('damage', only_to_me=False)
async def Damage(session: CommandSession):
    exp = Expression(session.current_arg_text.strip())
    try:
        damage = exp.parse()
    except IllegalExpressionError as e:
        await session.send('表达式非法：' + str(e))
    else:
        player = load_group(session.ctx['group_id']).get_player_from_sender(session.ctx['sender'])
        await session.send('HP={:.0f}-{:.0f}={:.0f}{}'.format(
            player.HP, damage, player.HP - damage, '，啊你死了' if damage >= player.HP else ''),
            at_sender=True)
        player.HP -= damage
        player.store()
