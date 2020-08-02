import nonebot
from nonebot import on_command, CommandSession


@on_command('help', aliases=('usage',))
async def help(session: CommandSession):
    plugins = list(filter(lambda p: p.name, nonebot.get_loaded_plugins()))
    arg = session.current_arg_text.strip().lower()
    if not arg:
        await session.send('目前支持的插件（回复help 插件名，查看插件具体使用帮助）：\n' +
                           '\n'.join(p.name for p in plugins))
        return

    for p in plugins:
        if p.name.lower() == arg:
            await session.send(p.usage)
