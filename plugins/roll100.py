from nonebot import on_command, CommandSession
from nonebot import permission as perm
from random import randint
from .GroupInfo import Group, load_group, SkillNotExistError, UserFileNotExistError

__plugin_name__ = 'roll100'
__plugin_usage__ = '''扔骰子，别名ra，用法为：
ra  （生成一个1-100的随机数）
ra 技能值  （根据技能值进行判定）
ra 技能名  （根据该用户已存储的技能进行判定）
ra 技能名 技能值  （根据输入的技能名和技能值进行判定，并会存储roll的技能）'''


@on_command('roll100', aliases=('ra',), only_to_me=False)
async def roll100(session: CommandSession):
    skill = session.state['skill']
    value = session.state['value']
    r = randint(1, 100)

    success = ''
    if value is not None:
        if r <= value / 5:
            success = '极困难成功'
        elif r <= value / 2:
            success = '困难成功'
        elif r <= value:
            success = '成功'
        else:
            success = '失败'
    if r <= 5:
        success = '大成功！'
    elif r > 95:
        success = '大失败！'

    player = session.state['player']
    if player is not None:
        player.store_roll(skill, value, success.strip('！'))
        player.store()

    await session.send('进行{}{:.0f}判定：\n1D100={:.0f}，{}'.format(
        skill, 100 if value is None else value, r, success
    ), at_sender=True)


@roll100.args_parser
async def _(session: CommandSession):
    args = session.current_arg_text.strip().split()

    if await perm.check_permission(session.bot, session.ctx, perm.GROUP):
        player = load_group(session.ctx['group_id']).get_player_from_sender(session.ctx['sender'])
    else:
        player = None

    skill = ''
    value = None
    if len(args) == 1:
        try:
            value = float(args[0])
        except ValueError:
            skill = args[0]
            try:
                value = player.get_skill(skill)
            except (SkillNotExistError, UserFileNotExistError):
                session.finish('你并未录入过技能：{}'.format(skill))
            except AttributeError:
                # player is None
                session.finish('根据技能名ra只能在群里进行')
    elif len(args) >= 2:
        skill, value = args[:2]
        try:
            value = float(value)
            player.update_skill({skill: value})
        except ValueError:
            session.finish('格式错误！（/ra 技能名 技能值）')
        except AttributeError:
            session.finish('指定技能名ra只能在群里进行')

    session.state['skill'] = skill
    session.state['value'] = value
    session.state['player'] = player
