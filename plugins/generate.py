from nonebot import on_command, CommandSession
from random import randint
from .GroupInfo import Group, load_group

__plugin_name__ = 'generate'
__plugin_usage__ = '''按规则车卡，生成三个之后由玩家选择，别名gen
回复generate rule查看车卡公式'''

MAX_WAIT_REPLY = 10


@on_command('generate', aliases=('gen',), only_to_me=False)
async def generateCard(session: CommandSession):
    skill_func = {
        '力量': lambda: sum([randint(1, 6) for _ in range(3)]) * 5,
        '体质': lambda: sum([randint(1, 6) for _ in range(3)]) * 5,
        '体型': lambda: (randint(1, 6) + 10) * 5,
        '敏捷': lambda: sum([randint(1, 6) for _ in range(3)]) * 5,
        '外貌': lambda: sum([randint(1, 6) for _ in range(3)]) * 5,
        '智力': lambda: (sum([randint(1, 6) for _ in range(2)]) + 6) * 5,
        '意志': lambda: sum([randint(1, 6) for _ in range(3)]) * 5,
        '教育': lambda: (sum([randint(1, 6) for _ in range(2)]) + 6) * 5,
        '幸运': lambda: sum([randint(1, 6) for _ in range(3)]) * 5,
    }

    if session.is_first_run:
        skills = [{key: func() for key, func in skill_func.items()} for _ in range(3)]
        session.state['skills'] = skills
        await session.send(
            '在{:d}次回复之内选择卡参数，回复abandon放弃\n'.format(MAX_WAIT_REPLY) +
            '选择属性：\n' +
            '\n'.join(
                [str(i) + '：' + '，'.join('{}{:d}'.format(key, value) for key, value in skill.items())
                 for i, skill in enumerate(skills)]),
            at_sender=True)
        session.state['user_id'] = session.ctx['user_id']
        session.state['reply_time'] = 0
        session.pause()
    else:
        skills_chosen = session.state['skills'][session.state['i']]
        player = load_group(session.ctx['group_id']).get_player(session.ctx['sender'])
        player.skill = skills_chosen
        player.store()
        await session.send('成功录入')


@generateCard.args_parser
async def _(session: CommandSession):
    rule = \
    '''力量 3D6后乘5
体质 3D6后乘5
体型 1D6+10后乘5
敏捷 3D6后乘5
外貌 3D6后乘5
智力 2D6+6后乘5
意志 3D6后乘5
教育 2D6+6后乘5
幸运 3D6后乘5
HP=floor((体质+体型)/10)'''

    if session.current_arg_text.strip() == 'rule':
        await session.send(rule)
        session.finish()

    if not session.is_first_run:
        if session.ctx['user_id'] != session.state['user_id']:
            session.pause()
        session.state['reply_time'] += 1
        if session.state['reply_time'] >= MAX_WAIT_REPLY or session.current_arg_text.strip() == 'abandon':
            session.finish()
        try:
            i = int(session.current_arg_text)
            if i > 3 or i < 0:
                raise Exception('list index exceeded')
            session.state['i'] = i
        except Exception as e:
            await session.send(str(e))
            session.pause()
