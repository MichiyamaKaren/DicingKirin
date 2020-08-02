from nonebot import on_command, CommandSession
from nonebot import permission as perm
from random import randint
from .GroupInfo import Group, load_group, SkillNotExistError, UserFileNotExistError

__plugin_name__ = 'secretroll(rh)'
__plugin_usage__ = '''暗骰，别名rh，用法和ra相同，但默认对心理学骰'''


@on_command('secretroll', aliases=('rh',), only_to_me=False)
async def SecretRoll(session: CommandSession):
    skill = session.state['skill']
    value = session.state['value']
    r = randint(1, 100)

    if r <= 5:
        success = '大成功！'
    elif r > 95:
        success = '大失败！'
    elif r <= value / 5:
        success = '极困难成功'
    elif r <= value / 2:
        success = '困难成功'
    elif r <= value:
        success = '成功'
    else:
        success = '失败'

    player = session.state['player']
    player.store_roll(skill, value, success.strip('！'))
    player.store()

    msg = '{}的暗骰，进行{}{:.0f}判定：\n1D100={:.0f}，{}'.format(
        player.name, skill, value, r, success
    )

    await session.bot.send_private_msg(user_id=session.state['KP'], message=msg)


@SecretRoll.args_parser
async def _(session: CommandSession):
    if not await perm.check_permission(session.bot, session.ctx, perm.GROUP):
        session.finish('暗骰只能在群里进行')

    group = load_group(session.ctx['group_id'])
    player = group.get_player_from_sender(session.ctx['sender'])

    if not group.KP:
        session.finish('进行暗骰之前，先指定KP')
    else:
        session.state['KP'] = group.KP

    args = session.current_arg_text.strip().split()

    skill = ''
    if len(args) == 0:
        skill = '心理学'
        try:
            value = player.get_skill(skill)
        except (SkillNotExistError, UserFileNotExistError):
            session.finish('你并未录入过心理学')
    elif len(args) == 1:
        try:
            value = float(args[0])
        except ValueError:
            skill = args[0]
            try:
                value = player.get_skill(skill)
            except (SkillNotExistError, UserFileNotExistError):
                session.finish('你并未录入过技能：{}'.format(skill))
    elif len(args) >= 2:
        skill, value = args[:2]
        try:
            value = float(value)
            player.update_skill({skill: value})
        except ValueError:
            session.finish('格式错误！（/ra 技能名 技能值）')

    session.state['skill'] = skill
    session.state['value'] = value
    session.state['player'] = player
