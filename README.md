基于 [nonebot](https://github.com/nonebot/nonebot) 的COC跑团机器人“骰鹿”。

---

## 2020.10.19更新
借由 [CQHTTP Mirai](https://github.com/yyuueexxiinngg/cqhttp-mirai) ，本项目可以原封不动地在 [mirai](https://github.com/mamoe/mirai) 平台上继续运行。感谢无论是为酷Q还是mirai贡献过的开发者们。

---

功能一览：

### 掷骰
- roll(r)：对随机表达式求值，如`/r 1d10`
- roll100(ra)：根据存储的技能值掷一个1d100骰子进行判定，也可以自行指定技能值，如`/ra 侦查`或`/ra 90`或`/ra 侦查 90`
- secretroll(rh)：暗骰，结果通过私聊发送给KP，默认为心理学，也可以为别的技能或指定技能值
- sancheck(sc)：san check，参数为用'/'分隔的两个随机表达式，如`/sc 0/1d4`

### 数据
- generate(gen)：生成人物基本属性
- store(st)：存储一个或多个技能值，如
```
/st 侦查 90
聆听 90
```
- list：查看已存储的技能和基本属性值
- clear：清除当前群中所有玩家数据
- damage：扣除HP，如`/damage 1d4`
- heal：回复HP，如`/heal 1d3`
- storeroll(stroll)：手动存储掷骰结果，如`/stroll 大成功 侦查 1`
- showroll：展示掷骰结果

### 配置
- setKP：设置KP（参数为QQ号或@KP）
- KPstate：KP通过此指令指定或切换自己扮演的npc的名字，从而可以扮演不止一名npc，如`/KPstate 张三`

### 帮助
- help(usage)：列出当前所有插件名，带参数指定插件可以列出该插件的使用说明，如`/help`或`/help roll`