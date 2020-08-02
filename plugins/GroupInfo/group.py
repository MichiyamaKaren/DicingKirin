import os
import shelve
from .player import Player


class Group:
    DATADIR = 'data'

    def __init__(self, group_id):
        self.group_id = group_id
        self.path = os.path.join(Group.DATADIR, str(group_id))
        if not os.path.exists(self.path):
            os.mkdir(self.path)
        self.players = {}
        self.npcs = set()

        self._KP = None
        self._KP_state = None
        self._updated = True

    def __del__(self):
        if self._updated:
            self.store()

    @property
    def KP(self):
        return self._KP

    @KP.setter
    def KP(self, value: int):
        self._updated = True
        self._KP = value

    @property
    def KP_state(self):
        return self._KP_state

    @KP_state.setter
    def KP_state(self, value):
        self._KP_state = value
        self._updated = True

    def get_player(self, sender):
        user_id = sender['user_id']
        if user_id not in self.players:
            self.players[user_id] = sender
            self._updated = True
        if sender['card']:
            name = sender['card']
        elif sender['nickname']:
            name = sender['nickname']
        else:
            name = str(user_id)
        return Player(name=name, group_path=self.path, user_id=user_id)

    def get_npc(self, name):
        if name not in self.npcs:
            self.npcs.add(name)
            self._updated = True
        return Player(name=name, group_path=self.path, filename='NPC' + name)

    def get_player_from_sender(self, sender):
        if (self.KP_state is not None) and sender['user_id'] == self.KP:
            return self.get_npc(self.KP_state)
        else:
            return self.get_player(sender)

    def store(self):
        self._updated = False
        with shelve.open(os.path.join(self.path, 'group')) as g:
            if 'group' in g:
                self.players.update(g['group'].players)
                self.npcs.update(g['group'].npcs)
            g['group'] = self

    def clear(self):
        for sender in self.players.values():
            self.get_player(sender).clear()
        for npc in self.npcs:
            self.get_npc(npc).clear()
        self.players = {}
        self._updated = True


def load_group(group_id):
    path = os.path.join(Group.DATADIR, str(group_id))
    if not os.path.exists(path):
        return Group(group_id)
    path = os.path.join(path, 'group')
    with shelve.open(path) as g:
        if 'group' in g:
            return g['group']
        else:
            return Group(group_id)
