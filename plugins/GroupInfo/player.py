import os
import json
from typing import Dict


class Player:
    def __init__(self, name, group_path, user_id=None, filename=None):
        self.name = name
        if filename:
            self.path = os.path.join(group_path, filename + '.json')
        elif user_id is not None:
            self.path = os.path.join(group_path, str(user_id) + '.json')

        self._skill: Dict = {}
        self._roll_history: Dict = {}
        self._loaded = False
        self._updated = False

    def __str__(self):
        fundamental = {'STR': '力量', 'CON': '体质', 'SIZ': '体型',
                       'DEX': '敏捷', 'APP': '外貌', 'INT': '智力',
                       'SAN': '意志', 'EDU': '教育', 'LUCK': '幸运',
                       'HP': 'HP', 'san': 'san', 'MP': 'MP'}
        return '{}：\n基础属性值：{}\n附加技能：{}'.format(
            self.name,
            '，'.join([attrname + '=' + str(self.__getattribute__(attr)) for attr, attrname in fundamental.items()]),
            '，'.join(['{}={:.0f}'.format(skill, value) for skill, value in self.skill.items() if
                      skill not in fundamental.values()])
        )

    def __del__(self):
        if self._updated:
            self.store()

    @property
    def skill(self):
        if not self._loaded:
            self.load()
        return self._skill

    @skill.setter
    def skill(self, value: Dict):
        if not self._loaded:
            # we need load the old value stored in json file first,
            # then replace self._skill by the parameter "value" here.
            # otherwise roll_history will be covered when this instance is stored.
            try:
                self.load()
            except UserFileNotExistError:
                pass
        self._skill = value
        self._updated = True

    @property
    def roll_history(self):
        if not self._loaded:
            self.load()
        return self._roll_history

    @property
    def STR(self):
        try:
            return self.get_skill('力量')
        except SkillNotExistError:
            self.update_skill({'力量': 0})
            return 0

    @STR.setter
    def STR(self, value):
        self.update_skill({'力量': value})

    @property
    def CON(self):
        try:
            return self.get_skill('体质')
        except SkillNotExistError:
            self.update_skill({'体质': 0})
            return 0

    @CON.setter
    def CON(self, value):
        self.update_skill({'体质': value})

    @property
    def SIZ(self):
        try:
            return self.get_skill('体型')
        except SkillNotExistError:
            self.update_skill({'体型': 0})
            return 0

    @SIZ.setter
    def SIZ(self, value):
        self.update_skill({'体型': value})

    @property
    def DEX(self):
        try:
            return self.get_skill('敏捷')
        except SkillNotExistError:
            self.update_skill({'敏捷': 0})
            return 0

    @DEX.setter
    def DEX(self, value):
        self.update_skill({'敏捷': value})

    @property
    def APP(self):
        try:
            return self.get_skill('外貌')
        except SkillNotExistError:
            self.update_skill({'外貌': 0})
            return 0

    @APP.setter
    def APP(self, value):
        self.update_skill({'外貌': value})

    @property
    def INT(self):
        try:
            return self.get_skill('智力')
        except SkillNotExistError:
            self.update_skill({'智力': 0})
            return 0

    @INT.setter
    def INT(self, value):
        self.update_skill({'智力': value})

    @property
    def SAN(self):
        try:
            return self.get_skill('意志')
        except SkillNotExistError:
            self.update_skill({'意志': 0})
            return 0

    @SAN.setter
    def SAN(self, value):
        self.update_skill({'意志': value})

    @property
    def san(self):
        try:
            return self.get_skill('san')
        except SkillNotExistError:
            self.update_skill({'san': self.SAN})
            return self.SAN

    @san.setter
    def san(self, value):
        self.update_skill({'san': value})

    @property
    def EDU(self):
        try:
            return self.get_skill('教育')
        except SkillNotExistError:
            self.update_skill({'教育': 0})
            return 0

    @EDU.setter
    def EDU(self, value):
        self.update_skill({'教育': value})

    @property
    def LUCK(self):
        try:
            return self.get_skill('幸运')
        except SkillNotExistError:
            self.update_skill({'幸运': 0})
            return 0

    @LUCK.setter
    def LUCK(self, value):
        self.update_skill({'幸运': value})

    @property
    def HP(self):
        try:
            return self.get_skill('HP')
        except SkillNotExistError:
            self.update_skill({'HP': self.maxHP})
            return self.get_skill('HP')

    @HP.setter
    def HP(self, value):
        self.update_skill({'HP': value})

    @property
    def MP(self):
        try:
            return self.get_skill('MP')
        except SkillNotExistError:
            self.update_skill({'MP': self.maxMP})
            return self.get_skill('MP')

    @MP.setter
    def MP(self, value):
        self.update_skill({'MP': value})

    @property
    def maxHP(self):
        return int((self.CON + self.SIZ) / 10)

    @property
    def maxMP(self):
        return int(self.SAN / 5)

    def heal(self, add):
        HP = self.HP + add
        HP = self.maxHP if HP > self.maxHP else HP
        self.HP = HP

    def update_skill(self, new_skill: Dict):
        try:
            _ = self.skill
        except UserFileNotExistError:
            # you can update skills even if you haven't yet stored a skill
            pass
        self._skill.update(new_skill)
        self._updated = True

    def get_skill(self, skillname):
        if skillname not in self.skill:
            raise SkillNotExistError(skillname)
        else:
            return self.skill[skillname]

    def store_roll(self, skill, value, success, n=1):
        if not success:
            return

        try:
            _ = self.roll_history
        except UserFileNotExistError:
            pass

        if not skill:
            skill = '（技能值{:.0f}）'.format(value)

        if success not in self._roll_history:
            self._roll_history[success] = {}
        if skill in self._roll_history[success]:
            self._roll_history[success][skill] += n
        else:
            self._roll_history[success][skill] = n
        self._updated = True

    def load(self):
        try:
            with open(self.path) as f:
                json_dict = json.load(f)
            self._skill = json_dict['skill']
            self._roll_history = json_dict['roll_history']
            self._loaded = True
        except FileNotFoundError:
            self._loaded = True
            raise UserFileNotExistError

    def store(self):
        with open(self.path, 'w') as f:
            json.dump({'skill': self._skill, 'roll_history': self._roll_history}, f)
        self._updated = False

    def clear(self):
        os.remove(self.path)


class UserFileNotExistError(Exception):
    pass


class SkillNotExistError(Exception):
    def __init__(self, skillname):
        self.skillname = skillname
