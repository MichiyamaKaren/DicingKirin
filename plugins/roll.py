from nonebot import on_command, CommandSession
from .Expression import Expression, IllegalExpressionError

__plugin_name__ = 'roll'
__plugin_usage__ = '''扔骰子，用法为：
roll/r 随机表达式 
随机表达式可以包含整数的加减运算，不支持括号，随机变量的格式为：
nDm：n个1-m的随机数之和'''


@on_command('roll', aliases=('r',), only_to_me=False)
async def roll(session: CommandSession):
    exp = Expression(session.current_arg_text.strip())
    try:
        result = exp.parse()
        await session.send('{}={:.0f}'.format(exp.exp, result), at_sender=True)
    except IllegalExpressionError as e:
        await session.send('表达式非法：' + str(e))
