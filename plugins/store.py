from nonebot import on_command, CommandSession
from nonebot import permission as perm
from .GroupInfo import Group, load_group, UserFileNotExistError

__plugin_name__ = 'store'
__plugin_usage__ = '存储技能值，用法为：store/st+技能，技能可以有多行，每条格式为：技能名 数值'


@on_command('store', aliases=('st',), only_to_me=False)
async def store(session: CommandSession):
    skills = session.state['skills']
    player = load_group(session.ctx['group_id']).get_player_from_sender(session.ctx['sender'])
    player.update_skill(skills)
    player.store()
    await session.send('成功存储技能：\n' +
                       '\n'.join(['{}：{:.0f}'.format(key, value) for key, value in skills.items()]),
                       at_sender=True)


@store.args_parser
async def _(session: CommandSession):
    lines = session.current_arg_text.strip('\n').split('\n')

    if not await perm.check_permission(session.bot, session.ctx, perm.GROUP):
        session.finish('只能在群聊中设置！')

    skills = {}
    try:
        for line in lines:
            key, value = line.split()
            skills[key] = int(value)
    except:
        await session.send('格式错误！')
    finally:
        session.state['skills'] = skills
