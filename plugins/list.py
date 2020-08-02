from nonebot import on_command, CommandSession
from nonebot import permission as perm
from .GroupInfo import Group, load_group, UserFileNotExistError, SkillNotExistError

__plugin_name__ = 'list'
__plugin_usage__ = '''显示所有已存储的属性'''


@on_command('list', only_to_me=False)
async def list(session: CommandSession):
    try:
        player = load_group(session.ctx['group_id']).get_player_from_sender(session.ctx['sender'])
        skills = session.state['skills']
        if skills:
            await session.send('，'.join([skill + '=' + str(player.get_skill(skill)) for skill in skills]),
                               at_sender=True)
        else:
            await session.send(str(player), at_sender=True)
    except SkillNotExistError as e:
        await session.send('你并未录入过技能：' + e.skillname, at_sender=True)
    except UserFileNotExistError:
        await session.send('你并未录入过技能', at_sender=True)


@list.args_parser
async def _(session: CommandSession):
    if await perm.check_permission(session.bot, session.ctx, perm.GROUP_MEMBER):
        session.state['skills'] = session.current_arg_text.strip().split()
    else:
        await session.send('只能在群聊中使用')
        session.finish()
