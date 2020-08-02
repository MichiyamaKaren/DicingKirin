from nonebot import on_command, CommandSession
from random import randint
from .Expression import Expression, IllegalExpressionError
from .GroupInfo import Group, load_group

__plugin_name__ = 'sancheck'
__plugin_usage__ = '''sancheck，用法为：
sancheck 随机表达式1/随机表达式2
掉san超过5会自动触发发狂判定'''


@on_command('sancheck', aliases=('sc',), only_to_me=False)
async def sancheck(session: CommandSession):
    player = load_group(session.ctx['group_id']).get_player_from_sender(session.ctx['sender'])
    try:
        e1, e2 = session.current_arg_text.strip().split('/')
        r = randint(1, 100)

        if r <= player.SAN:
            san_minus = Expression(e1).parse()
            success = '成功'
        else:
            san_minus = Expression(e2).parse()
            success = '失败'

        await session.send('进行理智{:.0f}判定：\n1D100={:d}，{}，san={:.0f}-{:.0f}={:.0f}'.format(
            player.SAN, r, success, player.san, san_minus, player.san - san_minus), at_sender=True)
        player.san -= san_minus
        player.store()

        if san_minus > 5 or san_minus >= player.SAN / 5:
            r = randint(1, 100)
            mad = r <= player.INT
            await session.send('掉san数值较大，进行智力{:.0f}判定：\n1D100={:d}，你{}'.format(
                player.INT, r, '发狂了' if mad else '没有发狂'
            ), at_sender=True)
            if mad:
                if san_minus > 5:
                    await temporary_mad(session)
                if san_minus >= player.SAN / 5:
                    await irregular_mad(session)
    except TypeError:
        await session.send('只能解析用\'/\'分隔的两个表达式')
    except IllegalExpressionError as e:
        await session.send('表达式非法：' + str(e))


async def temporary_mad(session: CommandSession):
    symptoms = {
        1: '昏厥或尖叫',
        2: '惊慌失措地逃跑',
        3: '歇斯底裡或情绪爆发(狂笑、哭泣等等)',
        4: '发出婴儿般的咿呀声，说话无条理、速语症、多语症',
        5: '强烈恐惧症，可能会定在当场不能动弹',
        6: '杀人犯罪倾向，或是自杀倾向',
        7: '出现幻觉或妄想症',
        8: '不自觉地模彷旁人的动作',
        9: '奇怪的食欲(泥土、黏土、人肉)',
        10: '恍惚(像胎儿一样蜷缩起来，忘记一切)或紧张型精神分裂(对一切失去兴趣，必须有别人引导，否则无法进行任何独立行动)'
    }
    r = randint(1, 10)
    await session.send('进入临时疯狂状态，1D10={:d}，症状为：\n{}'.format(r, symptoms[r]), at_sender=True)


async def irregular_mad(session: CommandSession):
    symptoms = {
        1: '记忆缺失、健忘(症)或恍惚(像胎儿一样蜷缩起来，忘记一切)或紧张型精神分裂(对一切失去兴趣，必须有别人引导，否则无法进行任何独立行动)',
        2: '严重的恐惧症(可能逃跑，或将所有东西都看成害怕的东西)',
        3: '幻觉',
        4: '奇怪的性取向(裸露癖、女子淫狂/男子淫狂等)',
        5: '找到了某样“幸运符”(把某样饰品、器物甚至某人当作安全毯)，如果远离就会一事无成',
        6: '无法控制地抽搐、颤抖，无法藉由语言或书写交谈',
        7: '精神性的失明、失聪，或某个肢体无法使用',
        8: '反应性精神障碍(语无伦次、幻觉、妄想症或行为异常)',
        9: '暂时的偏执狂',
        10: '强迫症(不停洗手、祈祷，以特定节奏走路，不愿走在某些路面上，总是检查子弹是否上膛等等)'
    }
    r = randint(1, 10)
    await session.send('进入不定期疯狂状态，1D10={:d}，症状为：\n{}'.format(r, symptoms[r]), at_sender=True)
